from itertools import chain
from typing import Optional, Tuple

import numpy as np
from scipy import sparse

from hoinetx.core.hypergraph import Hypergraph


def binary_incidence_matrix(hypergraph: Hypergraph, shape: Optional[Tuple[int]]) -> sparse.spmatrix:
    """Convert a list of hyperedges into a scipy sparse csc array.

    Parameters
    ----------
    hypergraph: instance of the class Hypergraph.
        Every hyperedge is represented as either a tuple or list of nodes.
    shape: the shape of the adjacency matrix, passed to the array constructor.
        If None, it is inferred.

    Returns
    -------
    The binary adjacency matrix representing the hyperedges.
    """
    # See docs:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csc_array.html
    hye_list = list(hypergraph.edge_list.keys())
    len_list = [0] + [len(hye) for hye in hye_list]
    indptr = np.cumsum(len_list)

    type_ = type(hye_list[0])
    indices = type_(chain(*hye_list))

    data = np.ones_like(indices)

    return sparse.csc_array((data, indices, indptr), shape=shape).tocsr()


def incidence_matrix(hypergraph: Hypergraph, shape: Optional[Tuple[int]]) -> sparse.spmatrix:
    binary_incidence = binary_incidence_matrix(hypergraph, shape)
    incidence = binary_incidence.multiply(hypergraph.get_weights()).tocsr()
    return incidence
