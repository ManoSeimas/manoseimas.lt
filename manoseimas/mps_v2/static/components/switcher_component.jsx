var Switcher = React.createClass({
  getInitialState: function () {
    return {
      active_tab: 'fractions'
    }
  },

  setActiveTab: function (tab_name) {
    var self = this;
    return function () {
      self.setState({ active_tab: tab_name })
    }
  },

  render: function () {
    var self = this;
    var tabs = {
      fractions: {
        row_component: FractionRow,
        endpoint: '/mp/fractions_json',
        keys: [
          {key: 'name', title: 'Pavadinimas', icon: undefined},
          {key: 'member_count', title: 'Frakcijos narių skaičius', icon: 'users icon'},
          {key: 'avg_statement_count', title: 'Aktyvumas diskusijose', icon: 'comment outline icon'},
          {key: 'avg_passed_law_project_ratio', title: 'Projektų teikimo sėkmė', icon: ''},
          {key: 'avg_vote_percentage', title: 'Dalyvavimas balsavimuose', icon: ''}
        ],
        name: 'Frakcijos'
      },
      mps: {
        row_component: PaliamentarianRow,
        endpoint: '/mp/mps_json',
        keys: [
          {key: 'full_name', title: 'Pavardė', icon: undefined},
          {key: 'statement_count', title: 'Aktyvumas diskusijose', icon: 'comment outline icon'},
          {key: 'passed_law_project_ratio', title: 'Projektų teikimo sėkmė', icon: ''},
          {key: 'vote_percentage', title: 'Dalyvavimas balsavimuose', icon: ''}
        ],
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
      }
    };

    var tab = tabs[this.state.active_tab];

    return (
      <div>
        <div className="switcher-component">
          <div className="ui zero margin center aligned grid">
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
                        sidebar_filter={tab.filter} />
        </div>
      </div>
    )
  }
});

React.render(
  <Switcher />,
  document.getElementById('fraction-filter-component')
);
