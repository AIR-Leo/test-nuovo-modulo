# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CompetenzaWidget(models.Model):
    _name = 'competenza.widget'
    _description = 'Widget per gestione competenze'

    ordine_id = fields.Many2one('sale.order', string='Ordine', required=True)
    anno_competenza = fields.Integer(string='Anno Competenza', required=True)
    percentuale_competenza = fields.Float(string='Percentuale Competenza', required=True, digits=(5,2))
    
    @api.constrains('percentuale_competenza')
    def _check_percentuale(self):
        for record in self:
            if record.percentuale_competenza < 0 or record.percentuale_competenza > 100:
                raise ValidationError('La percentuale deve essere tra 0 e 100')

# JavaScript per il widget frontend
class CompetenzaWidgetJS extends AbstractField {
    template: 'CompetenzaWidgetTemplate',
    events: {
        'click .open-modal': '_onOpenModal',
        'click .save-competenza': '_onSaveCompetenza',
        'input .percentuale-input': '_onPercentualeChange'
    },

    init: function() {
        this._super.apply(this, arguments);
        this.modalOpen = false;
    },

    _onOpenModal: function(ev) {
        this.modalOpen = true;
        this._renderModal();
    },

    _renderModal: function() {
        this.$modal = $(QWeb.render('CompetenzaWidgetModal', {
            ordine: this.recordData.ordine_id,
            anno: this.recordData.anno_competenza,
            percentuale: this.recordData.percentuale_competenza
        }));
        
        this.$modal.modal('show');
    },

    _onSaveCompetenza: function() {
        const data = {
            ordine_id: this.$modal.find('.ordine-select').val(),
            anno_competenza: parseInt(this.$modal.find('.anno-input').val()),
            percentuale_competenza: parseFloat(this.$modal.find('.percentuale-input').val())
        };

        this._rpc({
            model: 'competenza.widget',
            method: 'write',
            args: [[this.res_id], data],
        }).then(() => {
            this.$modal.modal('hide');
            this.trigger_up('reload');
        });
    }
}

registry.add('competenza_widget', CompetenzaWidgetJS);
