#
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.compat.tests.mock import patch
from units.modules.utils import set_module_args
from .mlnxos_module import TestMlnxosModule, load_fixture
from ansible.modules.network.mlnxos import mlnxos_facts


class TestMlnxosFacts(TestMlnxosModule):

    module = mlnxos_facts

    def setUp(self):
        super(TestMlnxosFacts, self).setUp()

        self.mock_run_command = patch.object(
            mlnxos_facts.FactsBase, "_show_cmd")
        self.run_command = self.mock_run_command.start()

    def tearDown(self):
        super(TestMlnxosFacts, self).tearDown()

        self.mock_run_command.stop()

    def load_fixtures(self, commands=None, transport=None):

        def load_from_file(*args, **kwargs):
            command = args[0]
            filename = "mlnxos_facts_%s.cfg" % command
            filename = filename.replace(' ', '_')
            filename = filename.replace('/', '7')
            output = load_fixture(filename)
            return output

        self.run_command.side_effect = load_from_file

    def test_mlnxos_facts_version(self):
        set_module_args(dict(gather_subset='version'))
        result = self.execute_module()
        facts = result.get('ansible_facts')
        self.assertEqual(len(facts), 2)
        version = facts['ansible_net_version']
        self.assertEqual(version['Product name'], 'MLNX-OS')

    def test_mlnxos_facts_modules(self):
        set_module_args(dict(gather_subset='modules'))
        result = self.execute_module()
        facts = result.get('ansible_facts')
        self.assertEqual(len(facts), 2)
        modules = facts['ansible_net_modules']
        self.assertIn("MGMT", modules)

    def test_mlnxos_facts_interfaces(self):
        set_module_args(dict(gather_subset='interfaces'))
        result = self.execute_module()
        facts = result.get('ansible_facts')
        self.assertEqual(len(facts), 2)
        interfaces = facts['ansible_net_interfaces']
        self.assertEqual(len(interfaces), 2)

    def test_mlnxos_facts_all(self):
        set_module_args(dict(gather_subset='all'))
        result = self.execute_module()
        facts = result.get('ansible_facts')
        self.assertEqual(len(facts), 4)
