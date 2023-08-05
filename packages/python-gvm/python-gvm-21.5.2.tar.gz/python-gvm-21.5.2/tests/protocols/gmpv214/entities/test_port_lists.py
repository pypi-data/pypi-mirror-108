# -*- coding: utf-8 -*-
# Copyright (C) 2021 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ...gmpv214 import Gmpv214TestCase
from ...gmpv208.entities.port_lists import (
    GmpClonePortListTestMixin,
    GmpCreatePortListTestMixin,
    GmpCreatePortRangeTestMixin,
    GmpDeletePortListTestMixin,
    GmpDeletePortRangeTestMixin,
    GmpGetPortListsTestMixin,
    GmpGetPortListTestMixin,
    GmpModifyPortListTestMixin,
)


class Gmpv214ClonePortListTestCase(GmpClonePortListTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CreatePortListTestCase(
    GmpCreatePortListTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214CreatePortRangeListTestCase(
    GmpCreatePortRangeTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214DeletePortListTestCase(
    GmpDeletePortListTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214DeletePortRangeTestCase(
    GmpDeletePortRangeTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214GetPortListTestCase(GmpGetPortListTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetPortListsTestCase(GmpGetPortListsTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ModifyPortListTestCase(
    GmpModifyPortListTestMixin, Gmpv214TestCase
):
    pass
