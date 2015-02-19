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

import common
import anyvcs

import os
import subprocess


class GitTest(common.VCSTest):
    vcs = 'git'

    @classmethod
    def setUpRepos(cls):
        cls.repo = anyvcs.create(cls.main_path, 'git')
        common.check_call(['git', 'clone', cls.main_path, cls.working_path])
        cls.check_call(['git', 'config', 'user.email', 'me@example.com'])
        cls.check_call(['git', 'config', 'user.name', 'Test User'])
        cls.main_branch = 'master'
        cls.working_head = 'master'
        for action in cls.setUpWorkingCopy(cls.working_path):
            action.doGit(cls)

    @classmethod
    def getAbsoluteRev(cls):
        try:
            return cls.check_output(['git', 'log', '-1', '--pretty=format:%H']).decode()
        except subprocess.CalledProcessError:
            return None

    @classmethod
    def export(cls, rev, path):
        os.mkdir(path)
        cmd1 = ['git', 'archive', rev]
        data = common.check_output(cmd1, cwd=cls.main_path)
        cmd2 = ['tar', '-x', '-C', path]
        p = subprocess.Popen(cmd2, stdin=subprocess.PIPE)
        p.communicate(data)
        if p.returncode != 0:
            raise subprocess.CalledProcessError(p.returncode, cmd2)


class GitWorkingCopyTest(GitTest):

    @classmethod
    def setUpRepos(cls):
        super(GitWorkingCopyTest, cls).setUpRepos()
        cls.repo = anyvcs.open(cls.working_path)


### EMPTY TEST ###

class EmptyTest(common.EmptyTest):
    def test_branches(self):
        result = self.repo.branches()
        correct = []
        self.assertEqual(common.normalize_heads(correct), common.normalize_heads(result))

    def test_tags(self):
        result = self.repo.tags()
        correct = []
        self.assertEqual(common.normalize_heads(correct), common.normalize_heads(result))

    def test_heads(self):
        result = self.repo.heads()
        correct = []
        self.assertEqual(common.normalize_heads(correct), common.normalize_heads(result))

    def test_log(self):
        result = self.repo.log()
        self.assertEqual(len(result), 0)


class GitEmptyTest(GitWorkingCopyTest, EmptyTest):
    pass


class GitWorkingCopyEmptyTest(GitWorkingCopyTest, EmptyTest):
    pass


### EMPTY WITH COMMITS TEST ###

class GitEmptyWithCommitsTest(GitTest, common.EmptyWithCommitsTest):
    pass


class GitWorkingCopyEmptyWithCommitsTest(GitWorkingCopyTest, common.EmptyWithCommitsTest):
    pass


### MISMATCHED FILE TYPE TEST ###

class GitMismatchedFileTypeTest(GitTest, common.MismatchedFileTypeTest):
    pass


class GitWorkingCopyMismatchedFileTypeTest(GitWorkingCopyTest, common.MismatchedFileTypeTest):
    pass


### EMPTY MAIN BRANCH TEST ###

class GitEmptyMainBranchTest(GitTest, common.EmptyMainBranchTest):
    pass


### BASIC TEST ###

class BasicTest(common.GitLikeBasicTest):
    def test_branches(self):
        result = self.repo.branches()
        correct = ['master']
        self.assertEqual(common.normalize_heads(correct), common.normalize_heads(result))

    def test_tags(self):
        result = self.repo.tags()
        correct = []
        self.assertEqual(common.normalize_heads(correct), common.normalize_heads(result))

    def test_heads(self):
        result = self.repo.heads()
        correct = ['master']
        self.assertEqual(common.normalize_heads(correct), common.normalize_heads(result))


class GitBasicTest(GitTest, BasicTest):
    pass


class GitWorkingCopyBasicTest(GitWorkingCopyTest, BasicTest):
    pass


### UNRELATED BRANCH TEST ###

class GitUnrelatedBranchTest(GitTest, common.UnrelatedBranchTest):
    pass


class GitWorkingCopyUnrelatedBranchTest(GitWorkingCopyTest, common.UnrelatedBranchTest):
    pass


### BRANCH TEST STEP 3 ###

class GitBranchTestStep3(GitTest, common.GitLikeBranchTestStep3):
    pass


class GitWorkingCopyBranchTestStep3(GitWorkingCopyTest, common.GitLikeBranchTestStep3):
    pass


### BRANCH TEST STEP 7 ###

class GitBranchTestStep7(GitTest, common.GitLikeBranchTestStep7):
    pass


class GitWorkingCopyBranchTestStep7(GitWorkingCopyTest, common.GitLikeBranchTestStep7):
    pass


### BRANCH TEST STEP 9 ###

class GitBranchTestStep9(GitTest, common.GitLikeBranchTestStep9):
    pass


class GitWorkingCopyBranchTestStep9(GitWorkingCopyTest, common.GitLikeBranchTestStep9):
    pass


### BRANCH TEST STEP 11 ###

class GitBranchTestStep11(GitTest, common.GitLikeBranchTestStep11):
    pass


class GitWorkingCopyBranchTestStep11(GitWorkingCopyTest, common.GitLikeBranchTestStep11):
    pass


### BRANCH TEST STEP 13 ###

class BranchTestStep13(common.GitLikeBranchTestStep13):
    def test_log_all(self):
        result = [self.revrev[x.rev] for x in self.repo.log()]
        correct = [15, 14, 13, 12, 11, 10, 8, 7, 5, 4, 2]
        self.assertEqual(correct, result)


class GitBranchTestStep13(GitTest, BranchTestStep13):
    pass


class GitWorkingCopyBranchTestStep13(GitWorkingCopyTest, BranchTestStep13):
    pass


### CACHE TEST ###

class GitCacheTest(GitTest, common.CacheTest):
    pass


class GitWorkingCopyCacheTest(GitWorkingCopyTest, common.CacheTest):
    pass


class GitUTF8EncodingTest(GitTest, common.UTF8EncodingTest):
    pass


# Don't do these tests for now because many systems won't have the latin1
# locale and the tests will fail.    Also, Mercurial and Subversion will fail
# by default if you give them non-UTF-8 strings.
#
#class GitLatin1EncodingTest(GitTest, common.Latin1EncodingTest): pass


### COPY TEST ###

class GitCopyTest(GitTest, common.CopyTest):
    pass


class GitWorkingCopyCopyTest(GitWorkingCopyTest, common.CopyTest):
    pass


### EMPTY COMMIT TEST ###

class GitEmptyCommitTest(GitTest, common.EmptyCommitTest):
    pass


class GitWorkingCopyEmptyCommitTest(GitWorkingCopyTest, common.EmptyCommitTest):
    pass


if __name__ == "__main__":
    common.unittest.main()
