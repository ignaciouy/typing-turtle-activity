#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

# List of all key properties in the keyboard layout description.
#
# Keyboard Layouts use a property inheritance scheme similar to CSS (cascading style sheets):
# - Keys inherit properties from their groups, if not explicitly set.
# - Groups inherit properties from the layout.
# - The layout inherits properties from defaults values defined below.
#
# Therefore it is possible to set any property once in the Layout, and have
# it automatically filter down to all Keys, yet still be able to override it
# individually per key.
KEY_PROPS = [
    # Name of the layout.
    { 'name': 'layout-name',  'default': '' },

    # Source dimensions of the layout.  
    # This is the coordinate system that key sizes and coordinates are defined in.  
    # It can be any units, for example inches, millimeters, percentages, etc.  
    { 'name': 'layout-width',  'default': 100 },
    { 'name': 'layout-height', 'default': 100 },

    # Name of the group.
    { 'name': 'group-name', 'default': '' },

    # Position of group in layout coordinates.
    { 'name': 'group-x',  'default': 0 },
    { 'name': 'group-y',  'default': 0 },

    # Layout algorithm for the group.
    # Possibilities are: 'horizontal', 'vertical', 'custom'.
    { 'name': 'group-layout', 'default': 'custom' },

    # Position of key in layout coordinates.  Used by 'custom' layout algorithm.
    { 'name': 'key-x',  'default': 0 },
    { 'name': 'key-y',  'default': 0 },

    # Dimensions of a key in the layout coordinates.
    { 'name': 'key-width',  'default': 0 },
    { 'name': 'key-height', 'default': 0 },

    # Gap between keys. Used by 'horizontal' and 'verical' layout algorithms.
    { 'name': 'key-gap', 'default': 0 },

    # Keyboard scan code for this key.
    { 'name': 'key-scan', 'default': 0 },

    # Text label to be displayed on keys which do not generate ASCII keys.
    { 'name': 'key-label', 'default': '' },

    # Character generated by the key, when no modifier keys are pressed.
    { 'name': 'key-normal', 'default': '' },

    # Character generated by the key with shift pressed.
    { 'name': 'key-shift', 'default': '' },
]

# This is an example keyboard layout.
#
# The keyboard layout is described by the following data structure. The structure
# has three levels: Layout, Groups, and Keys.  A Layout contains a list of Groups,
# each of which contains a list of Keys.  Groups are intended to be a way to collect
# related keys (e.g. nearby each other on the keyboard with similar properties)
# together.
#
# Entirely new keyboard layouts can be created just by copying this structure and
# modifying the following values, without changing the code.
DEFAULT_LAYOUT = {
    'layout-name': "default",

    'layout-width': 775,
    'layout-height': 300,

    'group-layout': 'horizontal',

    'key-width': 45,
    'key-height': 45,
    'key-gap': 5,

    'groups': [
	{
	    'group-name': "row0",
            'group-x': 10,
            'group-y': 10,

            'key-height': 35,

	    'keys': [
	     {'key-normal':"",'key-shift':""}, # Escape 
	     {'key-normal':"",'key-shift':""}, # Show Source
	     {'key-normal':"",'key-shift':"",'key-width':182}, # Zoom
	     {'key-normal':"",'key-shift':"",'key-width':182}, # Size 
	     {'key-normal':"",'key-shift':"",'key-width':181}, # Volume
	     {'key-normal':"",'key-shift':""}, # Window
	     {'key-normal':"",'key-shift':""}, # Frame
	    ]
	},
	{
	    'group-name': "row1",
            'group-x': 10,
            'group-y': 50,

	    'keys': [
	     {'key-scan':0x31,'key-normal':"`",'key-shift':"~",'key-width':35}, 
	     {'key-scan':0x0a,'key-normal':"1",'key-shift':"!"}, 
	     {'key-scan':0x0b,'key-normal':"2",'key-shift':"@"}, 
	     {'key-scan':0x0c,'key-normal':"3",'key-shift':"#"}, 
	     {'key-scan':0x0d,'key-normal':"4",'key-shift':"$"}, 
	     {'key-scan':0x0e,'key-normal':"5",'key-shift':"%"}, 
	     {'key-scan':0x0f,'key-normal':"6",'key-shift':"^"}, 
	     {'key-scan':0x10,'key-normal':"7",'key-shift':"&"}, 
	     {'key-scan':0x11,'key-normal':"8",'key-shift':"*"}, 
	     {'key-scan':0x12,'key-normal':"9",'key-shift':"("}, 
	     {'key-scan':0x13,'key-normal':"0",'key-shift':")"}, 
	     {'key-scan':0x14,'key-normal':"-",'key-shift':"_"}, 
	     {'key-scan':0x15,'key-normal':"=",'key-shift':"+",'key-width':65},
	     {'key-scan':0x16,'key-label':"erase",'key-width':95}
	    ]
	},
	{
	    'group-name': "row2",
            'group-x': 10,
            'group-y': 100,

	    'keys': [
	     {'key-scan':0x17,'key-label':"tab"},
	     {'key-scan':0x18,'key-normal':"q",'key-shift':"Q"}, 
	     {'key-scan':0x19,'key-normal':"w",'key-shift':"W"}, 
	     {'key-scan':0x1a,'key-normal':"e",'key-shift':"E"}, 
	     {'key-scan':0x1b,'key-normal':"r",'key-shift':"R"}, 
	     {'key-scan':0x1c,'key-normal':"t",'key-shift':"T"}, 
	     {'key-scan':0x1d,'key-normal':"y",'key-shift':"Y"}, 
	     {'key-scan':0x1e,'key-normal':"u",'key-shift':"U"}, 
	     {'key-scan':0x1f,'key-normal':"i",'key-shift':"I"}, 
	     {'key-scan':0x20,'key-normal':"o",'key-shift':"O"}, 
	     {'key-scan':0x21,'key-normal':"p",'key-shift':"P"}, 
	     {'key-scan':0x22,'key-normal':"[",'key-shift':"{"}, 
	     {'key-scan':0x23,'key-normal':"]",'key-shift':"}",'key-width':55},
	     {'key-scan':0x24,'key-label':"enter",'key-width':95,'key-height':95}
	    ]
	},
	{
	    'group-name': "row3",
            'group-x': 10,
            'group-y': 150,

	    'keys': [
	     {'key-scan':0x25,'key-label':"ctrl",'key-width':55},
	     {'key-scan':0x26,'key-normal':"a",'key-shift':"A"}, 
	     {'key-scan':0x27,'key-normal':"s",'key-shift':"S"}, 
	     {'key-scan':0x28,'key-normal':"d",'key-shift':"D"}, 
	     {'key-scan':0x29,'key-normal':"f",'key-shift':"F"}, 
	     {'key-scan':0x2a,'key-normal':"g",'key-shift':"G"}, 
	     {'key-scan':0x2b,'key-normal':"h",'key-shift':"H"},
	     {'key-scan':0x2c,'key-normal':"j",'key-shift':"J"}, 
	     {'key-scan':0x2d,'key-normal':"k",'key-shift':"K"}, 
	     {'key-scan':0x2e,'key-normal':"l",'key-shift':"L"}, 
	     {'key-scan':0x2f,'key-normal':";",'key-shift':":"}, 
	     {'key-scan':0x30,'key-normal':"'",'key-shift':")"}, 
	     {'key-scan':0x33,'key-normal':"\\",'key-shift':"|"}
	    ]
	},
	{
	    'group-name': "row4",
            'group-x': 10,
            'group-y': 200,

	    'keys': [
	     {'key-scan':0x32,'key-label':"shift",'key-width':75},
	     {'key-scan':0x34,'key-normal':"z",'key-shift':"Z"}, 
	     {'key-scan':0x35,'key-normal':"x",'key-shift':"X"}, 
	     {'key-scan':0x36,'key-normal':"c",'key-shift':"C"}, 
	     {'key-scan':0x37,'key-normal':"v",'key-shift':"V"}, 
	     {'key-scan':0x38,'key-normal':"b",'key-shift':"B"}, 
	     {'key-scan':0x39,'key-normal':"n",'key-shift':"N"},
	     {'key-scan':0x3a,'key-normal':"m",'key-shift':"M"}, 
	     {'key-scan':0x3b,'key-normal':",",'key-shift':"<"}, 
	     {'key-scan':0x3c,'key-normal':".",'key-shift':">"}, 
	     {'key-scan':0x3d,'key-normal':"/",'key-shift':"?"},
	     {'key-scan':0x3e,'key-label':"shift",'key-width':75},
	     {'key-scan':0x6f,'key-label':"",'key-shift':""}, # Up
	     {'key-label':"",'key-shift':""}, # Multiply
	    ]
	},
	{
	    'group-name': "row5",
            'group-x': 10,
            'group-y': 250,

	    'keys': [
	     {'key-label':"fn",'key-width':35},
	     {'key-label':"",'key-width':55}, # LHand
	     {'key-scan':0x40,'key-label':"alt",'key-width':55}, # LAlt
	     {'key-scan':0x41,'key-normal':" ",'key-shift':" ", 'key-width':325}, 
	     {'key-scan':0x6c,'key-label':"alt",'key-width':55}, # RAlt
	     {'key-label':"",'key-width':55}, # RHand
	     {'key-scan':0x71,'key-label':""}, # Left 
	     {'key-scan':0x74,'key-label':""}, # Down
	     {'key-scan':0x72,'key-label':""}, # Right
	    ]
	}
    ]
}

class Key:
    def __init__(self, props):
        self.props = props

        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

        self.screen_x = 0
        self.screen_y = 0
        self.screen_width = 0
        self.screen_height = 0

        self.pressed = False
        self.hilite = False

    def set_hilite(self, enabled):
        self.hilite = enabled

class Keyboard(gtk.EventBox):
    """A GTK widget which implements an interactive visual keyboard, with support
       for custom data driven layouts."""

    def __init__(self, root_window):
        gtk.EventBox.__init__(self)

        self.root_window = root_window

        self.area = gtk.DrawingArea()
        self.area.connect("expose-event", self._expose_cb)
        self.add(self.area)

        # This array contains the current keyboard layout.
        self.keys = None
        self.key_map = None

        self.shift_down = False

        # Setup keyboard event snooping in the root window.
        root_window.add_events(gtk.gdk.KEY_PRESS_MASK | gtk.gdk.KEY_RELEASE_MASK)
        root_window.connect('key-press-event', self._key_press_cb)
        root_window.connect('key-release-event', self._key_release_cb)

    def _build_key_list(self, layout):
        """Builds a list of Keys objects from a layout description.  
           Also fills in derived and inherited key properties.  
           The layout description can be discarded afterwards."""
        self.keys = []
        self.key_map = {}

        group_count = 0
        for g in layout['groups']:
            
            key_count = 0
            for k in g['keys']:

                # Create and fill out a unique property list for this key.
                props = k.copy()

                # Assign key and group index.
                props['key-index'] = key_count
                props['group-index'] = group_count

                # Inherit undefined properties from group, layout and
                # defaults, in that order.
                for p in KEY_PROPS:
                    pname = p['name']
                    if not props.has_key(pname):
                        if g.has_key(pname):
                            props[pname] = g[pname]
                        elif layout.has_key(pname):
                            props[pname] = layout[pname]
                        else:
                            props[pname] = p['default']

                # Add to internal list.
                key = Key(props)
                self.keys.append(key)
                key_count += 1
           
                # Add to scan code mapping table.
                if props['key-scan']:
                    self.key_map[props['key-scan']] = key

            group_count += 1
  
    def _layout_keys(self):
        """Assigns positions and sizes to the individual keys."""
        # Note- We know self.keys is sorted by group, and by index within the group.
        # The layout algorithms depend on this order.
        x, y = None, None
        cur_group = None
        for k in self.keys:
            # Reset the working coordinates with each new group.
            if k.props['group-index'] != cur_group:
                cur_group = k.props['group-index']
                x = k.props['group-x']
                y = k.props['group-y']
           
            # Apply the current layout.               
            if k.props['group-layout'] == 'horizontal':
                k.x = x
                k.y = y
                k.width = k.props['key-width']
                k.height = k.props['key-height']
                
                x += k.props['key-width']
                x += k.props['key-gap']

            elif k.props['group-layout'] == 'vertical':
                k.x = x
                k.y = y
                k.width = k.props['key-width']
                k.height = k.props['key-height']
                
                y += k.props['key-height']
                y += k.props['key-gap']

            elif k.props['group-layout'] == 'custom':
                k.x = x + k.props['key-x']
                k.y = y + k.props['key-y']
                k.width = k.props['key-width']
                k.height = k.props['key-height']

            else:
                k.x = 0
                k.y = 0
                k.width = 0
                k.height = 0

    def set_layout(self, layout):
        """Sets the keyboard's layout from  a layout description."""
        self._build_key_list(layout)
        self._layout_keys()

    def _update_screen_layout(self):
        """Applies the screen scaling factor for the layout given the current 
           allocation.
           TODO - Preserve the layout's aspect ratio in this calculation."""
        bounds = self.get_allocation()
 
        for k in self.keys:
            # This calculates a ratio from layout coordinates to the DrawingArea's
            # dimensions.  This ratio allows the layout coordinates to be *anything* -
            # inches, millimeters, percentage, whatever.  They just have to be
            # relative to layout-width and layout-height.
            ratio_x = 100 * bounds.width / k.props['layout-width']
            ratio_y = 100 * bounds.height / k.props['layout-height']

            # Make sure the final coordinates are integers, for the drawing routines.
            k.screen_x = int(k.x * ratio_x / 100)
            k.screen_y = int(k.y * ratio_y / 100)
            k.screen_width = int(k.width * ratio_x / 100)
            k.screen_height = int(k.height * ratio_y / 100)

    def _expose_cb(self, area, event):
        # Update layout given screen size.
        self._update_screen_layout()

        # Draw the keys.
        cr = self.area.window.cairo_create()
        cr.rectangle(event.area.x, event.area.y, event.area.width, event.area.height)
        cr.clip()

        for k in self.keys:
            cr.save()

            x1 = k.screen_x
            y1 = k.screen_y
            x2 = k.screen_x + k.screen_width
            y2 = k.screen_y + k.screen_height

            # Outline rounded box.
            corner = 5
            cr.move_to(x1 + corner, y1)
            cr.line_to(x2 - corner, y1)
            cr.line_to(x2, y1 + corner)
            cr.line_to(x2, y2 - corner)
            cr.line_to(x2 - corner, y2)
            cr.line_to(x1 + corner, y2)
            cr.line_to(x1, y2 - corner)
            cr.line_to(x1, y1 + corner)
            cr.close_path()

            if k.pressed:
                cr.set_source_rgb(1.0, 0.6, 0.6)
            elif k.hilite:
                cr.set_source_rgb(0.6, 1.0, 0.6)
            else:
                cr.set_source_rgb(1.0, 1.0, 1.0)
	    cr.fill_preserve()

            cr.set_source_rgb(0.1, 0.1, 0.1)
            cr.stroke_preserve()

            cr.clip()

            # Inner text.
            if k.props['key-label']:
                text = k.props['key-label']
            elif self.shift_down:
                text = k.props['key-shift']
            else:
                text = k.props['key-normal']

            cr.set_font_size(16)
            x_bearing, y_bearing, width, height = cr.text_extents(text)[:4]
    
            cr.move_to(x1+8 - x_bearing, y2-8 - height - y_bearing)
            cr.show_text(text)

            cr.restore()

        return True

    def _key_press_cb(self, widget, event):
        if self.key_map.has_key(event.hardware_keycode):
            key = self.key_map[event.hardware_keycode]
            key.pressed = True
            if key.props['key-label'] == 'shift':
                self.shift_down = True
 
        self.queue_draw()
        return False

    def _key_release_cb(self, widget, event):
        if self.key_map.has_key(event.hardware_keycode):
            key = self.key_map[event.hardware_keycode]
            key.pressed = False 
            if key.props['key-label'] == 'shift':
                self.shift_down = False

        self.queue_draw()
        return False

    def clear_hilite(self):
        for k in self.keys:
            k.hilite = False

    def find_key_by_letter(self, letter):
        for k in self.keys:
            if k.props['key-normal'] == letter or k.props['key-shift'] == letter:
                return k
        return None

if __name__ == "__main__":
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_title("keyboard widget")
    window.connect("destroy", lambda w: gtk.main_quit())

    k = Keyboard()
    k.set_layout(DEFAULT_LAYOUT)
    k.show()

    window.add(k)
    window.show()

    gtk.main()
