#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from cyphi.network import Network
from cyphi.subsystem import Subsystem

# TODO pass just the subsystem (contains a reference to the network)

no_connectivity = 0


def standard():
    """Matlab default network.

    Comes with subsystems attached, no assembly required.

    Diagram:

    |           +~~~~~~+
    |    +~~~~~>|   A  |<~~~~+
    |    |      | (OR) +~~~+ |
    |    |      +~~~~~~+   | |
    |    |                 | |
    |    |                 v |
    |  +~+~~~~~~+      +~~~~~+~+
    |  |   B    |<~~~~~+   C   |
    |  | (COPY) +~~~~~>| (XOR) |
    |  +~~~~~~~~+      +~~~~~~~+

    TPM:

    +~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+
    | Past state ~~> Current state |
    |~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~|
    |   A, B, C    |    A, B, C    |
    |~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~|
    |  {0, 0, 0}   |   {0, 0, 0}   |
    |  {0, 0, 1}   |   {1, 1, 0}   |
    |  {0, 1, 0}   |   {1, 0, 1}   |
    |  {0, 1, 1}   |   {1, 1, 1}   |
    |  {1, 0, 0}   |   {0, 0, 1}   |
    |  {1, 0, 1}   |   {1, 1, 1}   |
    |  {1, 1, 0}   |   {1, 0, 0}   |
    |  {1, 1, 1}   |   {1, 1, 0}   |
    +~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+

    Connectivity matrix:

    (CM_ij = 1 means that node i is connected to node j)

    |       A  B  C
    |     +~~~~~~~~~+
    |   A | 0, 0, 1 |
    |   B | 1, 0, 1 |
    |   C | 1, 1, 0 |
    |     +~~~~~~~~~+

    """
    # TODO? make these into dictionaries/named tuples
    current_state = (1, 0, 0)
    past_state = (1, 1, 0)
    tpm = np.array([[0, 0, 0],
                    [1, 1, 0],
                    [1, 0, 1],
                    [1, 1, 1],
                    [0, 0, 1],
                    [1, 1, 1],
                    [1, 0, 0],
                    [1, 1, 0]])

    cm = np.array([[0, 0, 1],
                   [1, 0, 1],
                   [1, 1, 0]])

    cm = None if no_connectivity else cm
    m = Network(tpm, current_state, past_state, connectivity_matrix=cm)
    return m


def subsys_n0n2():
    m = standard()
    return Subsystem([m.nodes[0], m.nodes[2]],
                     m.current_state,
                     m.past_state,
                     m)


def subsys_n1n2():
    m = standard()
    return Subsystem([m.nodes[1], m.nodes[2]],
                     m.current_state,
                     m.past_state,
                     m)


def s():
    m = standard()
    return Subsystem(m.nodes, m.current_state, m.past_state, m)


def simple():
    """ Simple 'AND' network.

    Diagram:

    |           +~~~~~~~+
    |    +~~~~~~+   A   |<~~~~+
    |    | +~~~>| (AND) +~~~+ |
    |    | |    +~~~~~~~+   | |
    |    | |                | |
    |    v |                v |
    |  +~+~+~~~~+      +~~~~~~+~+
    |  |   B    |<~~~~~+    C   |
    |  | (OFF)  +~~~~~>|  (OFF) |
    |  +~~~~~~~~+      +~~~~~~~~+

    TPM:

    +~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+
    |  Past state ~~> Current state |
    |~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~|
    |   A, B, C    |    A, B, C     |
    |~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~|
    |  {0, 0, 0}   |   {0, 0, 0}    |
    |  {0, 0, 1}   |   {0, 0, 0}    |
    |  {0, 1, 0}   |   {0, 0, 0}    |
    |  {0, 1, 1}   |   {1, 0, 0}    |
    |  {1, 0, 0}   |   {0, 0, 0}    |
    |  {1, 0, 1}   |   {0, 0, 0}    |
    |  {1, 1, 0}   |   {0, 0, 0}    |
    |  {1, 1, 1}   |   {0, 0, 0}    |
    +~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+
    """
    a_just_turned_on = (1, 0, 0)
    a_about_to_be_on = (0, 1, 1)
    tpm = np.array([[0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [1, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0]]).reshape([2] * 3 + [3]).astype(float)
    return Network(tpm, a_just_turned_on, a_about_to_be_on)


def s_subsys_all_off():
    s = simple()
    return Subsystem(s.nodes, (0, 0, 0), (0, 0, 0), s)


def s_subsys_all_a_just_on():
    s = simple()
    return Subsystem(s.nodes, s.current_state, s.past_state, s)


def big():
    """Return a large network."""
    tpm = np.array([[0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [1, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [1, 0, 0, 0, 0],
                    [1, 0, 0, 0, 1],
                    [1, 1, 0, 0, 1],
                    [0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 1],
                    [1, 1, 1, 0, 1],
                    [0, 0, 0, 1, 1],
                    [1, 0, 1, 1, 1],
                    [1, 0, 0, 1, 1],
                    [1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0],
                    [0, 1, 1, 0, 0],
                    [0, 1, 0, 0, 0],
                    [1, 1, 1, 0, 0],
                    [0, 0, 0, 1, 0],
                    [1, 1, 1, 1, 0],
                    [1, 1, 0, 1, 1],
                    [1, 1, 1, 1, 1],
                    [0, 0, 1, 1, 0],
                    [0, 1, 1, 1, 0],
                    [0, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [0, 0, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1]]).reshape([2] * 5 + [5]).astype(float)
    # All on
    current_state = (1,) * 5
    # All on
    past_state = (1,) * 5
    big = Network(tpm, current_state, past_state)
    return big


def big_subsys_all():
    """Return the subsystem associated with ``big``."""
    b = big()
    return Subsystem(b.nodes, b.current_state, b.past_state, b)


def reducible():
    tpm = np.zeros([2] * 2 + [2])
    current_state = (0, 0)
    past_state = (0, 0)
    cm = np.array([[1, 0],
                   [0, 1]])
    cm = None if no_connectivity else cm
    r = Network(tpm, current_state, past_state, connectivity_matrix=cm)
    # Return the full subsystem
    return Subsystem(r.nodes, current_state, past_state, r)
