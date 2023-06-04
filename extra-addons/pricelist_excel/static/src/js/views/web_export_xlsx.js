odoo.define('pricelist_excel.web_export_xlsx', function(require) {
	"use strict";

var form_widgets = require('web.form_widgets');

form_widgets.WidgetButton.include({
		on_click : function() {
			var self = this;
			this._super.apply(this, arguments);
			if (self.node.attrs.name == "export_excel") {
				self.view.enable_button();
				self.force_disabled = false;
				self.check_disable();
			}
		},

	});

});

