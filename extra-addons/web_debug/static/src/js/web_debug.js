odoo.define('web_debug.debug', function(require) {

"use strict";

    var Model = require('web.DataModel');
    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');
    var Users = new Model('res.users');

     var WKDebug = Widget.extend({
        template: 'WKDebug',
        events: {
            "click .oe_activate_debug_mode": "oe_activate_debug_mode",
        },
        oe_activate_debug_mode:  function (event){
            event.preventDefault();  
            window.location = $.param.querystring(window.location.href, 'debug');
        }, 
    });

     Users.call('has_group', ['base.group_system']).done(function(is_employee) {
        if (is_employee) {
             SystrayMenu.Items.push(WKDebug);
        }
    });

});