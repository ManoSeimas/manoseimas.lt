var FractionMemberList = React.createClass({
    render: function() {
        var keys = [
          {
              key: 'last_name',
              title: 'Pavardė',
              icon: undefined,
              order: 1
          },
          {
              key: 'vote_percentage',
              title: 'Dalyvavimas balsavimuose',
              explanation: 'Skaičiuojama, kokioje dalyje balsavimų Seimo narys dalyvavo (balsavo už, prieš arba susilaikė) nuo 2016 m. kadencijos pradžios.',
              icon: undefined,
              order: -1
          },
          {
              key: 'statement_count',
              title: 'Aktyvumas diskusijose',
              explanation: 'Skaičiuojama, kiek kartų Seimo narys pasisakė per Seimo plenarinius posėdžius nuo 2016 m. kadencijos pradžios.',
              icon: 'comment outline icon',
              order: -1
          },
          {
              key: 'passed_law_project_ratio',
              title: 'Projektų teikimo sėkmė',
              explanation: 'Skaičiuojama, kiek procentų teisės aktų projektų, kuriuos siūlė Seimo narys, buvo priimta.',
              icon: '',
              order: -1
          }
        ];
        var default_key = 'last_name';
        var default_order = 1;
        return (
          <div className='ui zero margin page grid active_tab'>
            <SortableList endpoint={this.props.endpoint}
                          rowComponent={PaliamentarianRow}
                          keys={keys}
                          default_key={default_key}
                          default_order={default_order}
                          sidebar_filter={undefined} />
          </div>
        )
    }

});

var endpoint = $('#fraction-member-list').attr("data-endpoint");

React.render(
  <FractionMemberList endpoint={endpoint} />,
  document.getElementById('fraction-member-list')
);
