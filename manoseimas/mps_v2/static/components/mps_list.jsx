var Mps = React.createClass({
    render: function () {
        var self = this;
        var tab = {
            row_component: PaliamentarianRow,
            endpoint: '/json/mps',
            keys: [{
                key: 'last_name',
                title: 'Pavardė',
                explanation: undefined,
                icon: undefined,
                order: 1
            }, {
                key: 'vote_percentage',
                title: 'Dalyvavimas balsavimuose',
                explanation: 'Skaičiuojama, kokioje dalyje balsavimų Seimo narys dalyvavo (balsavo už, prieš arba susilaikė) nuo 2016 m. kadencijos pradžios.',
                icon: '', order: -1
            }, {
                key: 'statement_count',
                title: 'Aktyvumas diskusijose',
                explanation: 'Skaičiuojama, kiek kartų Seimo narys pasisakė per Seimo plenarinius posėdžius nuo 2016 m. kadencijos pradžios.',
                icon: 'comment outline icon', order: -1
            }, {
                key: 'passed_law_project_ratio',
                title: 'Projektų teikimo sėkmė',
                explanation: 'Skaičiuojama, kiek procentų teisės aktų projektų, kuriuos siūlė Seimo narys, buvo priimta.',
                icon: '', order: -1
            }],
            default_key: 'last_name',
            default_order: 1,
            filter: {
                options_func: function (items) {
                    var options = {
                        all: {
                            name: 'Visos frakcijos',
                            logo_url: null
                        }
                    };
                    for (item of items) {
                        options[item.fraction_slug] = {
                            name: item.fraction_name,
                            logo_url: item.fraction_logo_url
                        };
                    };
                    return options
                },
                filter_func: function (item, option) {
                    return (option) ? (item.fraction_slug === option) : true
                }
            },
            name: 'Parlamentarai'
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
    <Mps />,
    document.getElementById('mps-list-component')
);
