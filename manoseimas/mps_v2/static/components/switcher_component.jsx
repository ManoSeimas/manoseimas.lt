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
        endpoint: '/json/fractions',
        keys: [
          {
            key: 'name',
            title: 'Pavadinimas',
            explanation: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit',
            icon: undefined,
            order: 1},
          {
            key: 'member_count',
            title: 'Frakcijos narių skaičius',
            explanation: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit',
            icon: 'users icon', order: -1},
          {
            key: 'avg_statement_count',
            title: 'Aktyvumas diskusijose',
            explanation: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit',
            icon: 'comment outline icon', order: -1},
          {
            key: 'avg_passed_law_project_ratio',
            title: 'Projektų teikimo sėkmė',
            explanation: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit',
            icon: '', order: -1},
          {
            key: 'avg_vote_percentage',
            title: 'Dalyvavimas balsavimuose',
            explanation: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit',
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
            explanation: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit',
            icon: undefined, order: 1},
          {
            key: 'statement_count',
            title: 'Aktyvumas diskusijose',
            explanation: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit',
            icon: 'comment outline icon', order: -1},
          {
            key: 'passed_law_project_ratio',
            title: 'Projektų teikimo sėkmė',
            explanation: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit',
            icon: '', order: -1},
          {
            key: 'vote_percentage',
            title: 'Dalyvavimas balsavimuose',
            explanation: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit',
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
