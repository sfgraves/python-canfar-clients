#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# ***********************************************************************
# ******************  CANADIAN ASTRONOMY DATA CENTRE  *******************
# *************  CENTRE CANADIEN DE DONNÉES ASTRONOMIQUES  **************
#
# (c) 2014.                            (c) 2014.
#  Government of Canada                 Gouvernement du Canada
#  National Research Council            Conseil national de recherches
#  Ottawa, Canada, K1A 0R6              Ottawa, Canada, K1A 0R6
#  All rights reserved                  Tous droits réservés
#
#  NRC disclaims any warranties,        Le CNRC dénie toute garantie
#  expressed, implied, or               énoncée, implicite ou légale,
#  statutory, of any kind with          de quelque nature que ce
#  respect to the software,             soit, concernant le logiciel,
#  including without limitation         y compris sans restriction
#  any warranty of merchantability      toute garantie de valeur
#  or fitness for a particular          marchande ou de pertinence
#  purpose. NRC shall not be            pour un usage particulier.
#  liable in any event for any          Le CNRC ne pourra en aucun cas
#  damages, whether direct or           être tenu responsable de tout
#  indirect, special or general,        dommage, direct ou indirect,
#  consequential or incidental,         particulier ou général,
#  arising from the use of the          accessoire ou fortuit, résultant
#  software.  Neither the name          de l'utilisation du logiciel. Ni
#  of the National Research             le nom du Conseil National de
#  Council of Canada nor the            Recherches du Canada ni les noms
#  names of its contributors may        de ses  participants ne peuvent
#  be used to endorse or promote        être utilisés pour approuver ou
#  products derived from this           promouvoir les produits dérivés
#  software without specific prior      de ce logiciel sans autorisation
#  written permission.                  préalable et particulière
#                                       par écrit.
#
#  This file is part of the             Ce fichier fait partie du projet
#  OpenCADC project.                    OpenCADC.
#
#  OpenCADC is free software:           OpenCADC est un logiciel libre ;
#  you can redistribute it and/or       vous pouvez le redistribuer ou le
#  modify it under the terms of         modifier suivant les termes de
#  the GNU Affero General Public        la “GNU Affero General Public
#  License as published by the          License” telle que publiée
#  Free Software Foundation,            par la Free Software Foundation
#  either version 3 of the              : soit la version 3 de cette
#  License, or (at your option)         licence, soit (à votre gré)
#  any later version.                   toute version ultérieure.
#
#  OpenCADC is distributed in the       OpenCADC est distribué
#  hope that it will be useful,         dans l’espoir qu’il vous
#  but WITHOUT ANY WARRANTY;            sera utile, mais SANS AUCUNE
#  without even the implied             GARANTIE : sans même la garantie
#  warranty of MERCHANTABILITY          implicite de COMMERCIALISABILITÉ
#  or FITNESS FOR A PARTICULAR          ni d’ADÉQUATION À UN OBJECTIF
#  PURPOSE.  See the GNU Affero         PARTICULIER. Consultez la Licence
#  General Public License for           Générale Publique GNU Affero
#  more details.                        pour plus de détails.
#
#  You should have received             Vous devriez avoir reçu une
#  a copy of the GNU Affero             copie de la Licence Générale
#  General Public License along         Publique GNU Affero avec
#  with OpenCADC.  If not, see          OpenCADC ; si ce n’est
#  <http://www.gnu.org/licenses/>.      pas le cas, consultez :
#                                       <http://www.gnu.org/licenses/>.
#
# ***********************************************************************

import os
import sys
import unittest
from datetime import datetime

# put local code at top of the search path
sys.path.insert(0, os.path.abspath('../../../'))

from canfar.groups.group import Group
from canfar.groups.group_property import GroupProperty
from canfar.groups.identity import Identity
from canfar.groups.user import User
from canfar.groups.group_xml.group_reader import GroupReader
from canfar.groups.group_xml.group_writer import GroupWriter

class TestGroupReaderWriter(unittest.TestCase):
    def test_minimal_group(self):
        expected = Group('groupID', None)
        writer = GroupWriter()
        xml_string = writer.write(expected, False)

        self.assertIsNotNone(xml_string)
        self.assertTrue(len(xml_string) > 0)

        reader = GroupReader()

        actual = reader.read(xml_string)

        self.assertIsNotNone(expected.group_id)
        self.assertIsNotNone(actual.group_id)
        self.assertEqual(actual.group_id, expected.group_id)

        self.assertIsNone(expected.owner)
        self.assertIsNone(actual.owner)

        self.assertIsNone(expected.description)
        self.assertIsNone(actual.description)

        self.assertIsNone(expected.last_modified)
        self.assertIsNone(actual.last_modified)

        self.assertItemsEqual(actual.group_members, expected.group_members)
        self.assertItemsEqual(actual.user_members, expected.user_members)
        self.assertItemsEqual(actual.group_admins, expected.group_admins)
        self.assertItemsEqual(actual.user_admins, expected.user_admins)

    def test_maximal_group(self):
        expected = Group('groupID', User(Identity('username', 'HTTP')))
        expected.description = 'description'
        expected.last_modified = datetime(2014, 01, 20, 19, 45, 37, 0)
        expected.properties.add(GroupProperty('key1', 'value1', True))
        expected.properties.add(GroupProperty('key2', 'value2', False))

        group_member1 = Group('groupMember1', User(Identity('uid1', 'UID')))
        group_member2 = Group('groupMember2', User(Identity('uid2', 'UID')))
        expected.group_members.add(group_member1)
        expected.group_members.add(group_member2)

        user_member1 = User(Identity('openid1', 'OpenID'))
        user_member2 = User(Identity('openid2', 'OpenID'))
        expected.user_members.add(user_member1)
        expected.user_members.add(user_member2)

        group_admin1 = Group('adminMember1', User(Identity('x5001', 'X500')))
        group_admin2 = Group('adminMember2', User(Identity('x5002', 'X500')))
        expected.group_admins.add(group_admin1)
        expected.group_admins.add(group_admin2)

        user_admin1 = User(Identity('foo1', 'HTTP'))
        user_admin2 = User(Identity('foo2', 'HTTP'))
        expected.user_admins.add(user_admin1)
        expected.user_admins.add(user_admin2)

        writer = GroupWriter()
        xml_string = writer.write(expected, True)

        self.assertIsNotNone(xml_string)
        self.assertTrue(len(xml_string) > 0)

        reader = GroupReader()
        actual = reader.read(xml_string)

        self.assertIsNotNone(expected.group_id)
        self.assertIsNotNone(actual.group_id)
        self.assertEqual(actual.group_id, expected.group_id)

        self.assertEqual(actual.owner.user_id.type, expected.owner.user_id.type)
        self.assertEqual(actual.owner.user_id.name, expected.owner.user_id.name)
        self.assertEqual(actual.description, expected.description)
        self.assertEqual(actual.last_modified, expected.last_modified)

        self.assertSetEqual(actual.properties, expected.properties)
        self.assertSetEqual(actual.group_members, expected.group_members)
        self.assertSetEqual(actual.user_members, expected.user_members)
        self.assertSetEqual(actual.group_admins, expected.group_admins)
        self.assertSetEqual(actual.user_admins, expected.user_admins)


def run():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGroupReaderWriter)
    return unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    run()
