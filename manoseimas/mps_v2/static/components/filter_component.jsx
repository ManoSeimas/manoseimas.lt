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
          {key: 'member_count', title: 'Frakcijos dydis', icon: 'users icon'},
          {key: 'avg_statement_count', title: 'Aktyvumas diskusijose', icon: 'comment outline icon'},
          {key: 'avg_passed_law_project_ratio', title: 'Projektai', icon: ''},
          {key: 'avg_vote_percentage', title: 'Balsavimai', icon: ''}
        ],
        name: 'Frakcijos'
      },
      mps: {
        row_component: PaliamentarianRow,
        endpoint: '/mp/mps_json',
        keys: [
          {key: 'second_name', title: 'Pavardė', icon: undefined},
          {key: 'statement_count', title: 'Aktyvumas diskusijose', icon: 'comment outline icon'},
          {key: 'passed_law_project_ratio', title: 'Projektai', icon: ''},
          {key: 'vote_percentage', title: 'Balsavimai', icon: ''}
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
        <div className='ui page grid active_tab'>
          <Filter endpoint={tab.endpoint} rowComponent={tab.row_component} keys={tab.keys} />
        </div>
      </div>
    )
  }
});


var Filter = React.createClass({
  getInitialState: function() {
    return {items: []};
  },

  componentDidMount: function() {
    if (this.isMounted()) this.loadData(this.props.endpoint);
  },

  loadData: function(endpoint) {
    $.get(endpoint, function(result) {
      this.setState({items: result.items});
    }.bind(this))
  },

  componentWillReceiveProps: function (nextProps) {
    this.loadData(nextProps.endpoint);
  },

  sortElements: function (param) {
    var self = this;
    return function () {
      self.setState({
        items: self.state.items.sort(function (a, b) {
          if (a[param] < b[param]) {
            return 1
          } else if (a[param] > b[param]) {
            return -1
          } else {
            return 0
          }
        })
      })
    }
  },

  render: function() {
    var sortkeys = this.props.keys;
    var self = this;

    return (
      <div>
        <div className="sort-keys">
          {sortkeys.map(function(sortkey) {
            return (
              <SortKeySelector params={sortkey} handler={self.sortElements(sortkey.key)} />
            )
          })}
        </div>
        <ElementList items={this.state.items} rowComponent={this.props.rowComponent} />
      </div>
    );
  }
});

var SortKeySelector = React.createClass({
  render: function() {
    return (
      <div className={this.props.params.active}>
        <a onClick={this.props.handler}>
          <i className={this.props.params.icon}></i>{this.props.params.title}
        </a>
      </div>
    )
  }
});

var ElementList = React.createClass({
  render: function() {
    var self = this;
    return (
      <div>
      {self.props.items.map(function (item) {
        return (
          <self.props.rowComponent obj={item} />
        )
      })}
      </div>
    );
  }
});


React.render(
  <Switcher />,
  document.getElementById('fraction-filter-component')
);

