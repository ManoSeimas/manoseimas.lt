var Switcher = React.createClass({

  getInitialState: function () {
    return {
      active_tab: 'mps',
      active_subtabs: { lobbyists: 'lobbyists' } //tabname: subtab_name
    }
  },

  setActiveTab: function (tab_name) {
    var self = this;
    return function () {
      self.setState({ active_tab: tab_name })
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
        default_subtab: 'lobbyists',
        lobbyists: {
          row_component: LobbyistRow,
          endpoint: 'lobbyists/json/lobbyists',
          default_key: 'law_project_count',
          default_order: -1,
          keys: [
            {
              key: 'slug',
              title: 'Pavadinimas',
              explanation: undefined,
              icon: undefined,
              order: 1},
            {
              key: 'law_project_count',
              title: 'Paveikti įstatymai',
              explanation: 'Skaičiuojamas bendras kiekis paveiktų teiės aktų.',
              icon: 'users icon', order: -1},
            {
              key: 'client_count',
              title: 'Užsakovai',
              explanation: undefined,
              icon: '', order: -1}
          ]
        },
        suggester: {
          row_component: SuggesterRow,
          endpoint: 'lobbyists/json/lobbyists',
          default_key: 'law_project_count',
          default_order: 1,
          keys: [
            {
              key: 'slug',
              title: 'Pavadinimas',
              explanation: undefined,
              icon: undefined,
              order: 1},
            {
              key: 'law_project_count',
              title: 'Paveikti įstatmai',
              explanation: 'Skaičiuojamas bendras kiekis paveiktų teiės aktų.',
              icon: 'users icon', order: -1},
            {
              key: 'number_of_suggestions',
              title: 'Teikta pastabų',
              explanation: 'Skaičiuojamas bendras kiekis teiktų pastabų visiems teisės aktams.',
              icon: '', order: -1}
          ]
        }
      }
    };
    return subtabs_by_tab[tab_name];
  },

  getSubtab: function (tab, subtab) {
    // Return a subtab subtab for tab tab.
    var self = this;
    subtabs = self.getSubtabs(tab);
    subtab = (subtab.startsWith('suggester') ? 'suggester' : subtab)
    return (subtab ? subtabs[subtab] : subtabs[subtabs.default_name]);
  },

  render: function () {
    var self = this;
    var active_subtabs = self.state.active_subtabs;
    var lobbyist_subtab = self.getSubtab('lobbyists', active_subtabs['lobbyists'])
    var tabs = {
      fractions: {
        row_component: FractionRow,
        endpoint: '/json/fractions',
        keys: [
          {
            key: 'name',
            title: 'Pavadinimas',
            explanation: undefined,
            icon: undefined,
            order: 1},
          {
            key: 'member_count',
            title: 'Frakcijos narių skaičius',
            explanation: undefined,
            icon: 'users icon', order: -1},
          {
            key: 'avg_vote_percentage',
            title: 'Dalyvavimas balsavimuose',
            explanation: 'Skaičiuojama, kokioje dalyje balsavimų kiekviena frakcija dalyvavo (balsavo už, prieš arba susilaikė) nuo 2012 m. kadencijos pradžios. Frakcijos dalyvavimas balsavimuose skaičiuojamas pagal kiekvieno frakcijos nario dalyvavimą, apskaičiavus jų vidurkį.',
            icon: '', order: -1},
          {
            key: 'avg_statement_count',
            title: 'Aktyvumas diskusijose',
            explanation: 'Skaičiuojama, kiek vidutiniškai kartų frakcijos narys pasisakė per Seimo plenarinius posėdžius metu. Skaičiuojami visi pasisakymai.',
            icon: 'comment outline icon', order: -1},
          {
            key: 'avg_passed_law_project_ratio',
            title: 'Projektų teikimo sėkmė',
            explanation: 'Skaičiuojama, kokia dalis iš visų frakcijos narių pateiktų teisės aktų projektų buvo priimti. Frakcijos priimtų projektų dalis skaičiuojama pagal kiekvieno frakcijos nario pateiktų ir priimtų teisės aktų projektų santykį, apskaičiavus jų vidurkį. Dėmesio! Kokia dalis pateiktų teisės aktų projektų bus priimti gali priklausyti nuo įvairių faktorių, pavyzdžiui, ar frakcija yra koalicijoje, ar opozicijoje.',
            icon: '', order: -1}
        ],
        default_key: 'name',
        default_order: 1,
        name: 'Frakcijos'
      },
      mps: {
        row_component: PaliamentarianRow,
        endpoint: '/json/mps',
        keys: [
          {
            key: 'last_name',
            title: 'Pavardė',
            explanation: undefined,
            icon: undefined, order: 1},
          {
            key: 'vote_percentage',
            title: 'Dalyvavimas balsavimuose',
            explanation: 'Skaičiuojama, kokioje dalyje balsavimų Seimo narys dalyvavo (balsavo už, prieš arba susilaikė) nuo 2012 m. kadencijos pradžios.',
            icon: '', order: -1},
          {
            key: 'statement_count',
            title: 'Aktyvumas diskusijose',
            explanation: 'Skaičiuojama, kiek kartų Seimo narys pasisakė per Seimo plenarinius posėdžius nuo 2012 m. kadencijos pradžios.',
            icon: 'comment outline icon', order: -1},
          {
            key: 'passed_law_project_ratio',
            title: 'Projektų teikimo sėkmė',
            explanation: 'Skaičiuojama, kiek procentų teisės aktų projektų, kuriuos siūlė Seimo narys, buvo priimta.',
            icon: '', order: -1}
        ],
        default_key: 'last_name',
        default_order: 1,
        filter: {
          options_func: function (items) {
            var options = {all: {
              name: 'Visos frakcijos',
              logo_url: null}
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
      },
      lobbyists: {
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
              lobbyists: {
                name: 'Lobistai',
                count: null
              },
              suggester_state: {
                name: 'Valstybė',
                count: null
              },
              suggester_other: {
                name: 'Kiti',
                count: null
              }
            };
            for (key of Object.keys(subtab_counts)) {
              options[key].count = subtab_counts[key];
            };
            return options
          },
          callback: this.setActiveSubtabs,
          active_subtab: this.state.active_subtabs.lobbyists
        },
        name: 'Lobistai'
      }
    };

    var tab = tabs[this.state.active_tab];
    return (
      <div>
        <div className="switcher-component">
          <div className="ui none margin center aligned grid">
            <div className="ui top attached tabular menu">
              {Object.keys(tabs).map(function (key) {
                var selected = (self.state.active_tab === key) ? 'active' : '';
                var class_names = 'item ' + selected;
                return (
                  <a className={class_names} onClick={self.setActiveTab(key)}>{tabs[key].name}</a>
                )
              })}
            </div>
          </div>
        </div>
        <div className='ui zero margin page grid active_tab'>
          <SortableList endpoint={tab.endpoint}
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

React.render(
  <Switcher />,
  document.getElementById('fraction-filter-component')
);
