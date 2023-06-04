odoo.define('set_home_action.set_home_action', function(require) {

"use strict";

    var Model = require('web.DataModel');
    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');
    var Users = new Model('res.users');

    var HAction = Widget.extend({
        template: 'set_home_action_tmpl',
        events: {
            "click .oe_set_home_action": "oe_set_home_action",
        },
        oe_set_home_action:  function (event){
            event.preventDefault();
            Users.call('set_home_action', [window.location.href]);
        }, 
    });
    Users.call('has_group', ['base.group_user']).done(function(is_employee) {
        if (is_employee) {
            SystrayMenu.Items.push(HAction);
        }
    });
    

});