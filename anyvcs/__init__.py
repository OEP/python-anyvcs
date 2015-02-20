# Copyright (c) 2013-2014, Clemson University
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name Clemson University nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from .version import __version__


def clone(srcpath, destpath, vcs=None, wc=False):
    """Clone an existing repository.

    :param str srcpath: Path to an existing repository
    :param str destpath: Desired path of new repository
    :param str vcs: Either ``git``, ``hg``, or ``svn``
    :param bool wc: Whether the resulting repo is a working copy.
    :returns VCSRepo: The newly cloned repository

    If ``vcs`` is not given, then the repository type is discovered from
    ``srcpath`` via :func:`probe`.

    """
    vcs, wc = _resolve_guess(srcpath, vcs, wc, False)
    cls = _get_repo_class(vcs, wc)
    return cls.clone(srcpath, destpath)


def create(path, vcs, wc=False):
    """Create a new repository

    :param str path: The path where to create the repository.
    :param str vcs: Either ``git``, ``hg``, or ``svn``
    :param bool wc: Whether the resulting repo is a working copy.

    """
    vcs, wc = _resolve_guess(path, vcs, wc, False)
    cls = _get_repo_class(vcs, wc)
    return cls.create(path)


def probe(path):
    """Probe a repository for its type.

    :param str path: The path of the repository
    :raises UnknownVCSType: if the repository type couldn't be inferred
    :returns str: either ``git``, ``hg``, or ``svn``

    This function employs some heuristics to guess the type of the repository.

    """
    vcs, wc = _probe(path)
    return vcs


def open(path, vcs=None, wc=None):
    """Open an existing repository

    :param str path: The path of the repository
    :param vcs: If specified, assume the given repository type to avoid
                auto-detection. Either ``git``, ``hg``, or ``svn``.
    :param bool wc: Skip auto-detection for working copies and assume given
                    value. If auto-detection is impossible, assumes the
                    repository is a working copy.
    :raises UnknownVCSType: if the repository type couldn't be inferred

    If ``vcs`` is not specified, it is inferred via :func:`probe`.

    """
    import os
    assert os.path.isdir(path), path + ' is not a directory'
    vcs, wc = _resolve_guess(path, vcs, wc, True)
    cls = _get_repo_class(vcs, wc)
    return cls(path)


def _get_repo_class(vcs, wc):
    assert wc in (True, False)
    from .common import UnknownVCSType
    if vcs == 'git':
        from .git import GitRepo, GitWorkingCopy
        return GitRepo if not wc else GitWorkingCopy
    elif vcs == 'hg':
        from .hg import HgRepo, HgWorkingCopy
        return HgRepo if not wc else HgWorkingCopy
    elif vcs == 'svn':
        from .svn import SvnRepo
        if wc:
            raise UnknownVCSType('%s (wc=True)' % vcs)
        return SvnRepo
    else:
        raise UnknownVCSType(vcs)


def _probe(path):
    import os
    from .common import UnknownVCSType
    if os.path.isdir(os.path.join(path, '.git')):
        return 'git', True
    elif os.path.isdir(os.path.join(path, '.hg')):
        return 'hg', None
    elif (
        os.path.isfile(os.path.join(path, 'config')) and
        os.path.isdir(os.path.join(path, 'objects')) and
        os.path.isdir(os.path.join(path, 'refs')) and
        os.path.isdir(os.path.join(path, 'branches'))
    ):
        return 'git', False
    elif (
        os.path.isfile(os.path.join(path, 'format')) and
        os.path.isdir(os.path.join(path, 'conf')) and
        os.path.isdir(os.path.join(path, 'db')) and
        os.path.isdir(os.path.join(path, 'locks'))
    ):
        return 'svn', False
    else:
        raise UnknownVCSType(path)


def _resolve_guess(path, vcs, wc, assume):
    '''
    Some common logic for resolving the VCS type and if the path points to a
    working copy.

    '''
    # If the user provided both to us, just use those.
    if not (vcs is None or wc is None):
        return vcs, wc

    # Otherwise, inspect the path and try to guess what the path is. `None`
    # here is a valid guess for `wc` because some repository working copies are
    # not trivially distiguishable from a normal repository. If nothing gives
    # any certainty, use the value of `assume`.
    vcs_guess, wc_guess = _probe(path)
    if vcs is None:
        vcs = vcs_guess
    if wc is None:
        wc = wc_guess if not wc_guess is None else assume

    return vcs, wc


# vi:set tabstop=4 softtabstop=4 shiftwidth=4 expandtab:
