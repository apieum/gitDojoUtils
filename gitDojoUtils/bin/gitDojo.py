# -*- coding: utf8 -*-
import os
import sys
import argparse


class GitDojo(object):
    commands = ['init', 'apply']

    def __init__(self):
        args = self._parseArgs()
        command = getattr(self, args.command, self._invalidCommand)
        command(args)

    def _parseArgs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("command", type=str, help="Command to execute", choices=self.commands, default="_invalidCommand")
        parser.add_argument("dir", nargs='?', help="git directory (default: current)", metavar='[DIR]', default=os.getcwd())
        return parser.parse_args()

    def _invalidCommand(self, args):
        print "ERROR: Command %s not exists." % args.command

    def init(self, args):
        repoDir = self._sanitizeRepoDir(args.dir)
        configFile = self._configFile(repoDir)
        if not os.path.exists(configFile):
            configFile = open(configFile, 'w')
            configFile.write(u"config = {\n}")
            configFile.close()

    def apply(self, args):
        repoDir = self._sanitizeRepoDir(args.dir)
        sys.path.insert(0, repoDir)
        import dojo
        self._applyHooks(dojo.config, repoDir)

    def _configFile(self, repoDir):
        return os.path.join(repoDir, "dojo.py")

    def _sanitizeRepoDir(self, repoDir):
        return os.path.realpath(repoDir)

    def _className(self, moduleName):
        return moduleName[0].upper() + moduleName[1:]

    def _applyHooks(self, hooks, repoDir):
        for hookName, hookConfig in hooks.items():
            hookContent = self._hookContent(repoDir, hookName, hookConfig['hook'])
            hookFile = self._hookFile(repoDir, hookName)
            self._writeHook(hookFile, hookContent)

    def _hookFile(self, repoDir, hookName):
        return os.path.join(repoDir, '.git', 'hooks', hookName)

    def _hookContent(self, repoDir, hookName, hookModule):
        return """#!/usr/bin/env python
import sys
sys.path.insert(0, '%s')
import dojo
from gitDojoUtils.hooks import %s
%s.%s(dojo.config['%s'])
""" % (repoDir, hookModule, hookModule, self._className(hookModule), hookName)

    def _writeHook(self, hookFile, hookContent):
        print "Write Hook %s" % hookFile
        hookFile = open(hookFile, 'w')
        hookFile.write(hookContent)
        hookFile.close()
