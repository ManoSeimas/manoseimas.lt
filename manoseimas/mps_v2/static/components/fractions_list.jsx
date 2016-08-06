var FractionsList = React.createClass({
    render: function () {
        var self = this;
        var tab = {
            row_component: FractionRow,
            endpoint: '/json/fractions',
            keys: [{
                key: 'name',
                title: 'Pavadinimas',
                explanation: undefined,
                icon: undefined,
                order: 1
            }, {
                key: 'member_count',
                title: 'Frakcijos narių skaičius',
                explanation: undefined,
                icon: 'users icon', order: -1
            }, {
                key: 'avg_vote_percentage',
                title: 'Dalyvavimas balsavimuose',
                explanation: 'Skaičiuojama, kokioje dalyje balsavimų kiekviena frakcija dalyvavo (balsavo už, prieš arba susilaikė) nuo 2012 m. kadencijos pradžios. Frakcijos dalyvavimas balsavimuose skaičiuojamas pagal kiekvieno frakcijos nario dalyvavimą, apskaičiavus jų vidurkį.',
                icon: '', order: -1
            }, {
                key: 'avg_statement_count',
                title: 'Aktyvumas diskusijose',
                explanation: 'Skaičiuojama, kiek vidutiniškai kartų frakcijos narys pasisakė per Seimo plenarinius posėdžius metu. Skaičiuojami visi pasisakymai.',
                icon: 'comment outline icon', order: -1
            }, {
                key: 'avg_passed_law_project_ratio',
                title: 'Projektų teikimo sėkmė',
                explanation: 'Skaičiuojama, kokia dalis iš visų frakcijos narių pateiktų teisės aktų projektų buvo priimti. Frakcijos priimtų projektų dalis skaičiuojama pagal kiekvieno frakcijos nario pateiktų ir priimtų teisės aktų projektų santykį, apskaičiavus jų vidurkį. Dėmesio! Kokia dalis pateiktų teisės aktų projektų bus priimti gali priklausyti nuo įvairių faktorių, pavyzdžiui, ar frakcija yra koalicijoje, ar opozicijoje.',
                icon: '', order: -1
            }],
            default_key: 'name',
            default_order: 1,
            name: 'Frakcijos'
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
    <FractionsList />,
    document.getElementById('filter-component')
);