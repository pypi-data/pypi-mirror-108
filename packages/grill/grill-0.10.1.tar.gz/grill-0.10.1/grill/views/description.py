"""Views related to USD scene description"""

import shutil
import tempfile
import subprocess
from pathlib import Path
from itertools import chain
from functools import lru_cache
from collections import defaultdict

import networkx as nx
from pxr import Usd, Pcp, Sdf
from networkx.drawing import nx_pydot
from PySide2 import QtWidgets, QtGui, QtCore, QtWebEngineWidgets

from . import sheets as _sheets


@lru_cache(maxsize=None)
def _dot_exe():
    return shutil.which("dot")


@lru_cache(maxsize=None)
def _dot_2_svg(sourcepath):
    print(f"Creating svg for: {sourcepath}")
    targetpath = f"{sourcepath}.svg"
    dotargs = [_dot_exe(), sourcepath, "-Tsvg", "-o", targetpath]
    kwargs = {}
    if hasattr(subprocess, 'CREATE_NO_WINDOW'):  # not on linux
        kwargs.update(creationflags=subprocess.CREATE_NO_WINDOW)
    result = subprocess.run(dotargs, capture_output=True, **kwargs)
    error = result.stderr.decode() if result.returncode else None
    return error, targetpath


class _Dot2SvgSignals(QtCore.QObject):
    error = QtCore.Signal(str)
    result = QtCore.Signal(str)


class _Dot2Svg(QtCore.QRunnable):
    def __init__(self, source_fp, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signals = _Dot2SvgSignals()
        self.source_fp = source_fp

    @QtCore.Slot()
    def run(self):
        if not _dot_exe():
            self.signals.error.emit(
                "In order to display composition arcs in a graph,\n"
                "the 'dot' command must be available on the current environment.\n\n"
                "Please make sure graphviz is installed and 'dot' available \n"
                "on the system's PATH environment variable."
            )
            return
        error, svg_fp = _dot_2_svg(self.source_fp)
        self.signals.error.emit(error) if error else self.signals.result.emit(svg_fp)


class _DotViewer(QtWidgets.QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QtWidgets.QVBoxLayout()
        self._graph_view = QtWebEngineWidgets.QWebEngineView(parent=self)
        self._error_view = QtWidgets.QTextBrowser()
        layout.addWidget(self._graph_view)
        layout.addWidget(self._error_view)
        layout.setContentsMargins(0, 0, 0, 0)
        self._error_view.setVisible(False)
        self.setLayout(layout)
        self.urlChanged = self._graph_view.urlChanged
        self._dot2svg = None
        self._threadpool = QtCore.QThreadPool()
        # otherwise it seems invisible
        self.resize(QtCore.QSize(self.height() + 100, self.width()))

    def setDotPath(self, path):
        if self._dot2svg:  # forget about previous, unfinished runners
            self._dot2svg.signals.error.disconnect()
            self._dot2svg.signals.result.disconnect()

        self._dot2svg = dot2svg = _Dot2Svg(path, parent=self)
        dot2svg.signals.error.connect(self._on_dot_error)
        dot2svg.signals.result.connect(self._on_dot_result)
        self._threadpool.start(dot2svg)

    def _on_dot_error(self, message):
        self._error_view.setVisible(True)
        self._graph_view.setVisible(False)
        self._error_view.setText(message)

    def _on_dot_result(self, filepath):
        self._error_view.setVisible(False)
        self._graph_view.setVisible(True)
        self._graph_view.load(QtCore.QUrl.fromLocalFile(filepath))


class _GraphViewer(_DotViewer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.urlChanged.connect(self._graph_url_changed)
        self.sticky_nodes = list()
        self._graph = None

    @property
    def url_id_prefix(self):
        return "_node_id_"

    def _graph_url_changed(self, url: QtCore.QUrl):
        node_uri = url.toString()
        node_uri_stem = node_uri.split("/")[-1]
        if node_uri_stem.startswith(self.url_id_prefix):
            index = node_uri_stem.split(self.url_id_prefix)[-1]
            if not index.isdigit():
                raise ValueError(f"Expected suffix of node URL ID to be a digit. Got instead '{index}' of type: {type(index)}.")
            self.view([int(index)])

    @lru_cache(maxsize=None)
    def _subgraph_dot_path(self, node_indices: tuple):
        print(f"Getting subgraph for: {node_indices}")
        graph = self.graph
        successors = chain.from_iterable(
            graph.successors(index) for index in node_indices)
        predecessors = chain.from_iterable(
            graph.predecessors(index) for index in node_indices)
        nodes_of_interest = list(self.sticky_nodes)  # sticky nodes are always visible
        nodes_of_interest.extend(chain(node_indices, successors, predecessors))
        subgraph = graph.subgraph(nodes_of_interest)

        fd, fp = tempfile.mkstemp()
        nx_pydot.write_dot(subgraph, fp)

        return fp

    def view(self, node_indices: list):
        dot_path = self._subgraph_dot_path(tuple(node_indices))
        self.setDotPath(dot_path)

    @property
    def graph(self):
        return self._graph

    @graph.setter
    def graph(self, graph):
        self._subgraph_dot_path.cache_clear()
        self.sticky_nodes.clear()
        self._graph = graph


class PrimComposition(QtWidgets.QDialog):
    _COLUMNS = {
        "Target Layer": lambda arc: arc.GetTargetNode().layerStack.identifier.rootLayer.identifier,
        "Target Path": lambda arc: arc.GetTargetNode().path,
        "Arc": lambda arc: arc.GetArcType().displayName,
        "Has Specs": Usd.CompositionArc.HasSpecs,
        "Is Ancestral": Usd.CompositionArc.IsAncestral,
        "Is Implicit": Usd.CompositionArc.IsImplicit,
        "From Root Layer Prim Spec": Usd.CompositionArc.IsIntroducedInRootLayerPrimSpec,
        "From Root Layer Stack": Usd.CompositionArc.IsIntroducedInRootLayerStack,
    }

    def __init__(self, *args, **kwargs):
        """For inspection and debug purposes, this widget makes primary use of:

            - Usd.PrimCompositionQuery  (similar to USDView's composition tab)
            - Pcp.PrimIndex.DumpToString
            - Pcp.PrimIndex.DumpToDotGraph  (when dot is available)
        """
        super().__init__(*args, **kwargs)
        self.index_box = QtWidgets.QTextBrowser()
        self.index_box.setLineWrapMode(self.index_box.NoWrap)
        self.composition_tree = tree = QtWidgets.QTreeWidget()
        tree.setColumnCount(len(self._COLUMNS))
        tree.setHeaderLabels([k for k in self._COLUMNS])
        tree.setAlternatingRowColors(True)
        self._dot_view = _DotViewer(parent=self)
        vertical = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        vertical.addWidget(tree)
        vertical.addWidget(self._dot_view)
        horizontal = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        horizontal.addWidget(vertical)
        horizontal.addWidget(self.index_box)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(horizontal)
        self.setLayout(layout)
        self.setWindowTitle("Prim Composition")

    def clear(self):
        self.composition_tree.clear()
        self.index_box.clear()

    def setPrim(self, prim):
        prim_index = prim.GetPrimIndex()
        self.index_box.setText(prim_index.DumpToString())
        tree = self.composition_tree
        tree.clear()
        query = Usd.PrimCompositionQuery(prim)
        tree_items = dict()  # Sdf.Layer: QTreeWidgetItem
        for arc in query.GetCompositionArcs():
            strings = [str(getter(arc)) for getter in self._COLUMNS.values()]
            intro_layer = arc.GetIntroducingLayer()
            if intro_layer and intro_layer in tree_items:
                parent = tree_items[intro_layer]
            else:
                parent = tree
            target_layer = arc.GetTargetNode().layerStack.identifier.rootLayer
            tree_items[target_layer] = QtWidgets.QTreeWidgetItem(parent, strings)

        tree.expandAll()
        fd, fp = tempfile.mkstemp()
        prim_index.DumpToDotGraph(fp)
        self._dot_view.setDotPath(fp)


class LayerStackComposition(QtWidgets.QDialog):
    _LAYERS_COLUMNS = (
        _sheets._Column("Layer Identifier", Sdf.Layer.identifier.getter),
    )

    _PRIM_COLUMNS = (
        _sheets._Column("Spec on Prim Path", lambda prim: str(prim.GetPath)),
    )

    def __init__(self, stage=None, parent=None, **kwargs):
        super().__init__(parent=parent, **kwargs)
        options = _sheets._ColumnOptions.SEARCH
        self._layers = _sheets._Spreadsheet(self._LAYERS_COLUMNS, options)
        self._prims = _sheets._Spreadsheet(self._PRIM_COLUMNS, options)

        for each in self._layers, self._prims:
            each.layout().setContentsMargins(0,0,0,0)
            each.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        horizontal = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        horizontal.addWidget(self._layers)
        horizontal.addWidget(self._prims)

        self._graph_view = _GraphViewer(parent=self)

        vertical = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        vertical.addWidget(horizontal)
        vertical.addWidget(self._graph_view)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(vertical)

        self.setLayout(layout)
        self.setStage(stage or Usd.Stage.CreateInMemory())
        self.setWindowTitle("Layer Stack Composition")

        selectionModel = self._layers.table.selectionModel()
        selectionModel.selectionChanged.connect(self._selectionChanged)
        self._paths = dict()

    def _selectionChanged(self, selected: QtCore.QItemSelection, deselected: QtCore.QItemSelection):
        node_ids = [index.data() for index in self._layers.table.selectedIndexes()]
        node_indices = [self._node_index_by_id[i] for i in node_ids]
        paths = set(chain.from_iterable(self._paths[i] for i in node_ids))

        prims_model = self._prims.model
        prims_model.clear()
        prims_model.setHorizontalHeaderLabels([''] * len(self._PRIM_COLUMNS))
        prims_model.setRowCount(len(paths))
        prims_model.blockSignals(True)
        for row_index, path in enumerate(paths):
            for column_index, getter in enumerate(self._LAYERS_COLUMNS):
                item = QtGui.QStandardItem()
                item.setData(path, QtCore.Qt.DisplayRole)
                item.setData(path, QtCore.Qt.UserRole)
                prims_model.setItem(row_index, column_index, item)
        prims_model.blockSignals(False)
        self._prims.table.resizeColumnsToContents()
        self._prims.table.horizontalHeader()._updateVisualSections(0)
        self._graph_view.view(node_indices)

    @_sheets.wait()
    def setStage(self, stage):
        """Sets the USD stage the spreadsheet is looking at."""
        self._stage = stage
        for table in self._layers, self._prims:
            table.model.clear()
            table.table.setSortingEnabled(False)

        # labels are on the header widgets
        self._layers.model.setHorizontalHeaderLabels([''] * len(self._LAYERS_COLUMNS))
        self._prims.model.setHorizontalHeaderLabels([''] * len(self._PRIM_COLUMNS))

        self._graph_view.graph = graph = nx.DiGraph(tooltip="LayerStack Composition")
        # we always want to see the legend nodes, so mark them as sticky
        self._graph_view.sticky_nodes = legend_node_ids = list()
        # legend
        arcs_to_display = {  # should include all?
            Pcp.ArcTypePayload: dict(color=10, colorscheme="paired12", fontcolor=10),  # purple
            Pcp.ArcTypeReference: dict(color=6, colorscheme="paired12", fontcolor=6),  # red
            Pcp.ArcTypeVariant: dict(color=8, colorscheme="paired12", fontcolor=8),  # yellow
            Pcp.ArcTypeSpecialize: dict(color=12, colorscheme="paired12", fontcolor=12),  # brown
            Pcp.ArcTypeInherit: dict(color=4, colorscheme="paired12", fontcolor=4),  # green
        }

        for arc_type, edge_attrs in arcs_to_display.items():
            label = f" {arc_type.displayName}"
            arc_node_indices = (len(legend_node_ids), len(legend_node_ids)+1)
            graph.add_nodes_from(arc_node_indices, style='invis')
            graph.add_edge(*arc_node_indices, label=label, **edge_attrs)
            legend_node_ids.extend(arc_node_indices)

        layer_stacks_by_node_idx = dict()
        stack_id_by_node_idx = dict.fromkeys(legend_node_ids)  # {42: layer.identifier}
        self._node_index_by_id = node_index_by_id = dict.fromkeys(legend_node_ids)  # {layer.identifier: 42}

        self._paths = paths = defaultdict(set)  # {layer.identifier: {path1, ..., pathN}}

        def _layer_label(layer):
            return Path(layer.realPath).stem or layer.identifier

        def _walk_layer_tree(tree):
            tree_layer = tree.layer
            if tree_layer:
                yield tree_layer
            for childtree in tree.childTrees:
                yield from _walk_layer_tree(childtree)

        def _add_node(pcp_node):
            layer_stack = pcp_node.layerStack
            root_layer = layer_stack.identifier.rootLayer
            root_id = root_layer.identifier
            if root_id in node_index_by_id:
                return
            stack_index = len(stack_id_by_node_idx)

            node_index_by_id[root_id] = stack_index
            stack_id_by_node_idx[stack_index] = root_id
            label = f"{{{_layer_label(root_layer)}"
            sublayers = [layer for layer in _walk_layer_tree(layer_stack.layerTree)]
            layer_stacks_by_node_idx[stack_index] = sublayers
            for layer in sublayers:
                if layer == root_layer:
                    continue
                node_index_by_id[layer.identifier] = stack_index
                label += f"|{_layer_label(layer)}"
            label += "}"
            ids = '\n'.join(f"{i}: {layer.realPath or layer.identifier}" for i, layer in enumerate(sublayers))
            tooltip = f"Layer Stack:\n{ids}"
            # https://stackoverflow.com/questions/16671966/multiline-tooltip-for-pydot-graph
            tooltip = tooltip.replace('\n', '&#10;')
            graph.add_node(stack_index, style='rounded', shape='record', label=label,
                       tooltip=tooltip, title='world', href=f"{self._graph_view.url_id_prefix}{stack_index}")

        # only query composition arcs that have specs on our prims.
        qFilter = Usd.PrimCompositionQuery.Filter()
        qFilter.hasSpecsFilter = Usd.PrimCompositionQuery.HasSpecsFilter.HasSpecs

        for prim in stage.TraverseAll():
            path_str = str(prim.GetPath())
            query = Usd.PrimCompositionQuery(prim)
            query.filter = qFilter

            for arc in query.GetCompositionArcs():
                _add_node(arc.GetTargetNode())
                target = arc.GetTargetNode().layerStack.identifier.rootLayer
                target_id = target.identifier
                target_stack_idx = node_index_by_id[target_id]
                for layer in layer_stacks_by_node_idx[node_index_by_id[target_id]]:
                    paths[layer.identifier].add(path_str)
                intro = arc.GetIntroducingLayer()
                if intro:
                    assert intro.identifier in node_index_by_id, f"Expected {intro} to be on {node_index_by_id.keys()}"
                    edge_attrs = arcs_to_display[arc.GetArcType()]
                    source_stack_idx = node_index_by_id[intro.identifier]
                    graph.add_edge(source_stack_idx, target_stack_idx, **edge_attrs)

        layers_model = self._layers.model
        def _createItem(layer):
            item = QtGui.QStandardItem(layer.identifier)
            item.setData(layer, QtCore.Qt.UserRole)
            return item
        items_to_add = [
            # QtGui.QStandardItem(layer.identifier)
            _createItem(layer)
            for node_id in sorted(set(graph.nodes).difference(legend_node_ids))
            for layer in layer_stacks_by_node_idx[node_id]
            if layer  # ensure the layer is still valid, (e.g. not expired)
        ]
        layers_model.setRowCount(len(items_to_add))
        layers_model.blockSignals(True)  # prevent unneeded events from computing
        for index, item in enumerate(items_to_add):
            layers_model.setItem(index, 0, item)

        layers_model.blockSignals(False)
        for table in self._layers, self._prims:
            table.table.setSortingEnabled(True)
