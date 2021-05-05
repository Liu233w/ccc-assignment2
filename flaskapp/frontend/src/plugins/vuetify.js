import Vue from 'vue';
import Vuetify from 'vuetify/lib';

Vue.use(Vuetify);

export default new Vuetify({
                             theme: {
                               themes: {
                                 light: {
                                   primary: '#454551',
                                   secondary: '#ec0b6d',
                                   accent: '#00b0c5',
                                   error: '#ed1b2f',
                                   info: '#33a3dc',
                                   success: '#9fd645',
                                   warning: '#faa519'
                                 },
                               },
                             },
                           })
