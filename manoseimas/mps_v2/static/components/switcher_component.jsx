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
          {key: 'avg_passed_law_project_ratio', title: 'Projektų teikimas', icon: ''},
          {key: 'avg_vote_percentage', title: 'Dalyvavimas balsavimuose', icon: ''}
        ],
        name: 'Frakcijos'
      },
      mps: {
        row_component: PaliamentarianRow,
        endpoint: '/mp/mps_json',
        keys: [
          {key: 'second_name', title: 'Pavardė', icon: undefined},
          {key: 'statement_count', title: 'Aktyvumas diskusijose', icon: 'comment outline icon'},
          {key: 'passed_law_project_ratio', title: 'Projektų teikimas', icon: ''},
          {key: 'vote_percentage', title: 'Dalyvavimas balsavimuose', icon: ''}
        ],
        name: 'Parlamentarai'
      }
    };
    var tab = tabs[this.state.active_tab];

    return (
      <div>
        <div className="colored-bg">
          <div className="ui zero margin center aligned grid">
            <div className="switcher">
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
          <Filter endpoint={tab.endpoint} rowComponent={tab.row_component} keys={tab.keys} />
        </div>
      </div>
    )
  }
});

React.render(
  <Switcher />,
  document.getElementById('fraction-filter-component')
);
