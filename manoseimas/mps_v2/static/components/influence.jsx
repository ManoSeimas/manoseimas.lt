var Influence = React.createClass({

    getInitialState: function () {
        return {
            active_subtabs: { lobbyists: 'suggester_other' } //tab_name: subtab_name
        }
    },

    setActiveSubtabs: function (tab_name, subtab_name) {
        // A callback to switch subtab that can be passed down the hierarchy.
        var self = this;
        self.setState(function(previousState, currentProps) {
            var new_subtabs = {};
            var old_subtabs = previousState.active_subtabs;
            Object.keys(old_subtabs).map( function(key) {
                key === tab_name ? val = subtab_name : val = old_subtabs[key];
                new_subtabs[key] = val;
            });
            return {active_subtabs: new_subtabs};
        });
    },

    getSubtabs: function (tab_name) {
        // Return subtabs for a given tab.
        var subtabs_by_tab = {
            lobbyists: {
                lobbyists: {
                    row_component: LobbyistRow,
                    endpoint: 'lobbyists/json/lobbyists',
                    default_key: 'law_project_count',
                    default_order: -1,
                    keys: [{
                        key: 'slug',
                        title: 'Pavadinimas',
                        explanation: undefined,
                        icon: undefined,
                        order: 1
                    }, {
                        key: 'law_project_count',
                        title: 'Siekta paveikti įstatymus',
                        explanation: 'Skaičiuojamas bendras kiekis paveiktų teisės aktų.',
                        icon: 'users icon', order: -1
                    },{
                        key: 'client_count',
                        title: 'Užsakovai',
                        explanation: undefined,
                        icon: '', order: -1
                    }]
                },
                suggester_state: {
                    row_component: SuggesterRow,
                    endpoint: 'json/suggesters/?state_actor=1',
                    default_key: 'suggestion_count',
                    default_order: -1,
                    keys: [{
                        key: 'slug',
                        title: 'Pavadinimas',
                        explanation: undefined,
                        icon: undefined,
                        order: 1
                    }, {
                        key: 'law_project_count',
                        title: 'Siekta paveikti įstatymus',
                        explanation: 'Skaičiuojamas bendras kiekis paveiktų teisės aktų.',
                        icon: 'users icon', order: -1
                    }, {
                        key: 'suggestion_count',
                        title: 'Teikta pastabų',
                        explanation: 'Skaičiuojamas bendras kiekis teiktų pastabų visiems teisės aktams.',
                        icon: '', order: -1
                    }]
                },
                suggester_other: {
                    row_component: SuggesterRow,
                    endpoint: 'json/suggesters/?state_actor=0',
                    default_key: 'suggestion_count',
                    default_order: -1,
                    keys: [{
                        key: 'slug',
                        title: 'Pavadinimas',
                        explanation: undefined,
                        icon: undefined,
                        order: 1
                    }, {
                        key: 'law_project_count',
                        title: 'Siekta paveikti įstatymus',
                        explanation: 'Skaičiuojamas bendras kiekis paveiktų teisės aktų.',
                        icon: 'users icon', order: -1
                    }, {
                        key: 'suggestion_count',
                        title: 'Teikta pastabų',
                        explanation: 'Skaičiuojamas bendras kiekis teiktų pastabų visiems teisės aktams.',
                        icon: '', order: -1
                    }]
                }
            }
        };
        return subtabs_by_tab[tab_name]
    },

    getSubtab: function (tab, subtab) {
        // Return a subtab subtab for tab tab.
        var subtabs = this.getSubtabs(tab);
        return subtabs[subtab];
    },

    render: function () {
        var active_subtabs = this.state.active_subtabs;
        var lobbyist_subtab = this.getSubtab('lobbyists', active_subtabs['lobbyists'])

        var tab = {
            keys: lobbyist_subtab.keys,
            row_component: lobbyist_subtab.row_component,
            endpoint: lobbyist_subtab.endpoint,
            default_key: lobbyist_subtab.default_key,
            default_order: lobbyist_subtab.default_order,
            subtabs: {
                options_func: function (subtab_counts) {
                    var options = {
                        header: {
                            name: 'Daro įtaką',
                            count: null
                        },
                        suggester_other: {
                            name: 'Suinteresuoti asmenys',
                            count: null
                        },
                        suggester_state: {
                            name: 'Valdžios atstovai',
                            count: null
                        },
                        lobbyists: {
                            name: 'Registruoti lobistai',
                            count: null
                        }
                    };

                    for (key of Object.keys(subtab_counts)) {
                        options[key].count = subtab_counts[key];
                    }

                    return options
                },
                callback: this.setActiveSubtabs,
                active_subtab: this.state.active_subtabs.lobbyists
            },
            name: 'Įtaka'
        };

        return (
            <div>
                <div className='ui zero margin page grid active_tab'>
                    <SortableList
                        endpoint={tab.endpoint}
                        rowComponent={tab.row_component}
                        keys={tab.keys}
                        default_key={tab.default_key}
                        default_order={tab.default_order}
                        sidebar_filter={tab.filter}
                        sidebar_subtabs={tab.subtabs}/>
                </div>
            </div>
        )
    }
});

ReactDOM.render(
    <Influence />,
    document.getElementById('filter-component')
);