#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2002-2006  Donald N. Allingham
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

# $Id: _FilterList.py 6529 2006-05-03 06:29:07Z rshura $

from gettext import gettext as _
import gtk
import GrampsWidgets
import RelLib

from _SidebarFilter import SidebarFilter
from Filters.Rules.Person import *
from Filters import GenericFilter

class PersonSidebarFilter(SidebarFilter):

    def __init__(self, clicked):
        SidebarFilter.__init__(self)
        self.clicked_func = clicked

    def create_widget(self):
        self.filter_name = gtk.Entry()
        self.filter_id = gtk.Entry()
        self.filter_birth = gtk.Entry()
        self.filter_death = gtk.Entry()
        self.filter_event = RelLib.Event()
        self.filter_event.set_type((RelLib.EventType.CUSTOM,''))
        self.etype = gtk.ComboBoxEntry()
        
        self.event_menu = GrampsWidgets.MonitoredDataType(
            self.etype,
            self.filter_event.set_type,
            self.filter_event.get_type)
        
        self.filter_note = gtk.Entry()
        self.filter_gender = gtk.combo_box_new_text()
        for i in [ _('any'), _('male'), _('female'), _('unknown') ]:
            self.filter_gender.append_text(i)
        self.filter_gender.set_active(0)
            
        self.filter_regex = gtk.CheckButton(_('Use regular expressions'))

        self.add_text_entry(_('Name'), self.filter_name)
        self.add_text_entry(_('ID'), self.filter_id)
        self.add_entry(_('Gender'), self.filter_gender)
        self.add_text_entry(_('Birth date'), self.filter_birth)
        self.add_text_entry(_('Death date'), self.filter_death)
        self.add_entry(_('Has Event'), self.etype)
        self.add_text_entry(_('Note'), self.filter_note)
        self.add_entry(None, self.filter_regex)

    def clear(self, obj):
        self.filter_name.set_text('')
        self.filter_id.set_text('')
        self.filter_birth.set_text('')
        self.filter_death.set_text('')
        self.filter_note.set_text('')
        self.filter_gender.set_active(0)
        self.etype.child.set_text('')

    def clicked(self, obj):
        self.clicked_func()

    def get_filter(self):
        name = self.filter_name.get_text().strip()
        gid = self.filter_id.get_text().strip()
        birth = self.filter_birth.get_text().strip()
        death = self.filter_death.get_text().strip()
        note = self.filter_note.get_text().strip()
        gender = self.filter_gender.get_active()
        regex = self.filter_regex.get_active()

        if not name and not gid and not birth and not death \
               and not str(self.filter_event.get_type()) and \
               not note and not gender > 0:
            generic_filter = None
        else:
            generic_filter = GenericFilter()
            if name:
                if regex:
                    rule = RegExpName([name])
                else:
                    rule = SearchName([name])
                generic_filter.add_rule(rule)
            if gid:
                if regex:
                    rule = RegExpIdOf([gid])
                else:
                    rule = MatchIdOf([gid])
                generic_filter.add_rule(rule)
            if gender > 0:
                if gender == 1:
                    generic_filter.add_rule(IsMale([]))
                elif gender == 2:
                    generic_filter.add_rule(IsFemale([]))
                else:
                    generic_filter.add_rule(HasUnknownGender([]))

            etype = self.filter_event.get_type()
            if str(etype):
                rule = HasEvent([etype, '', '', ''])
                generic_filter.add_rule(rule)
                
            if birth:
                rule = HasBirth([birth,'',''])
                generic_filter.add_rule(rule)
            if death:
                rule = HasDeath([death,'',''])
                generic_filter.add_rule(rule)
            if note:
                if regex:
                    rule = HasNoteRegexp([note])
                else:
                    rule = HasNoteMatchingSubstringOf([note])
                generic_filter.add_rule(rule)
        return generic_filter

