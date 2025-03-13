/*! Foundation integration for DataTables' Editor
 * © SpryMedia Ltd - datatables.net/license
 */

import jQuery from 'jquery';
import DataTable from 'datatables.net-zf';
import Editor from 'datatables.net-editor';

// Allow reassignment of the $ variable
let $ = jQuery;


/*
 * Set the default display controller to be our foundation control 
 */
DataTable.Editor.defaults.display = "foundation";


/*
 * Change the default classes from Editor to be classes for Foundation
 */
$.extend( true, DataTable.Editor.classes, {
	field: {
		wrapper:         "DTE_Field row",
		label:           "small-4 columns inline",
		input:           "small-8 columns DTE_Field_Input",
		error:           "error",
		multiValue:      "panel radius multi-value",
		multiInfo:       "small",
		multiRestore:    "panel radius multi-restore",
		"msg-labelInfo": "label secondary",
		"msg-info":      "label secondary",
		"msg-message":   "label secondary",
		"msg-error":     "label alert"
	},
	form: {
		button:  "button small",
		buttonInternal:  "button small",
		buttonSubmit: 'button small'
	}
} );


/*
 * Foundation display controller - this is effectively a proxy to the Foundation
 * modal control.
 */
var shown = false;
var reveal;

// Get the Foundation library from DT or local
function getFoundation() {
	let dtF = DataTable.use('foundation');

	if (dtF) {
		return dtF;
	}

	if (window.Foundation) {
		return window.Foundation;
	}

	throw new Error('No Foundation library. Set it with `DataTable.use(foundation);`');
}

const dom = {
	content: $(
		'<div class="reveal reveal-modal DTED" data-reveal></div>'
	),
	close: $('<button class="close close-button">&times;</div>')
};

DataTable.Editor.fieldTypes.autocomplete.dropDownBody = true;
DataTable.Editor.fieldTypes.tags.dropDownBody = true;

DataTable.Editor.display.foundation = $.extend( true, {}, DataTable.Editor.models.displayController, {
	init: function () {
		if (! reveal) {
			let foundation = getFoundation();

			reveal = new foundation.Reveal( dom.content, {
				closeOnClick: false
			} );
		}

		return DataTable.Editor.display.foundation;
	},

	open: function ( dte, append, callback ) {
		var content = dom.content;
		content.children().detach();
		content.append( append );
		content.prepend( dom.close );

		dom.close
			.attr('title', dte.i18n.close)
			.off('click.dte-zf')
			.on('click.dte-zf', function () {
				dte.close('icon');
			});

		$(document)
			.off('click.dte-zf')
			.on('click.dte-zf', 'div.reveal-modal-bg, div.reveal-overlay', function (e) {
				if ( $(e.target).closest(dom.content).length ) {
					return;
				}
				dte.background();
			} );

		if ( shown ) {
			if ( callback ) {
				callback();
			}
			return;
		}

		shown = true;

		$(dom.content)
			.one('open.zf.reveal', function () {
				if ( callback ) {
					callback();
				}
			});

		reveal.open();
	},

	close: function ( dte, callback ) {
		if (shown) {
			reveal.close();
			shown = false;
		}

		if ( callback ) {
			callback();
		}
	},

	node: function () {
		return dom.content[0];
	}
} );


export default DataTable.Editor;
