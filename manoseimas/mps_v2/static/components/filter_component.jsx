var Switcher = React.createClass({
  getInitialState: function () {
    return {
      active_tab: 'fractions'
    }
  },

  render: function () {
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
        row_component: FractionRow,  // XXX change it!!!
        endpoint: '/mp/mps_json',
        keys: [
          {key: 'name', title: 'Pavadinimas', icon: undefined},
          {key: 'avg_statement_count', title: 'Aktyvumas diskusijose', icon: 'comment outline icon'},
          {key: 'avg_passed_law_project_ratio', title: 'Projektai', icon: ''},
          {key: 'avg_vote_percentage', title: 'Balsavimai', icon: ''}
        ],
        name: 'Parlamentarai'
      }
    };

    var tab = tabs[this.state.active_tab];
    console.log('tab', tab);
    return (
      <div>
        <div className="tabs">
          <a className="tab">Fractions</a>
          <a className="tab">Parliamentarians</a>
        </div>
        <div className='active_tab'>
          <Filter endpoint={tab.endpoint} rowComponent={tab.row_component} keys={tab.keys} />
        </div>
      </div>
    )
  }
})

var Filter = React.createClass({
  getInitialState: function() {
    return {
      items: []
    };
  },

  componentDidMount: function() {
    $.get('/mp/fractions_json', function(result) {
      if (this.isMounted()) {
        this.setState({
          items: result.fractions
        });
      }
    }.bind(this))
  },

  sortElements: function (param) {
    var self = this;
    return function () {
      self.setState({
        items: self.state.items.sort(function (a, b) {
          if (a[param] > b[param]) {
            return 1
          } else if (a[param] < b[param]) {
            return -1
          } else {
            return 0
          }
        })
      })
    }
  },

  render: function() {
    var sortkeys = [
      {key: 'name', title: 'Pavadinimas', icon: undefined},
      {key: 'member_count', title: 'Frakcijos dydis', icon: 'users icon'},
      {key: 'avg_statement_count', title: 'Aktyvumas diskusijose', icon: 'comment outline icon'},
      {key: 'avg_passed_law_project_ratio', title: 'Projektai', icon: ''},
      {key: 'avg_vote_percentage', title: 'Balsavimai', icon: ''}
    ]
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

var FractionRow = React.createClass({
  render: function() {
    var fraction = this.props.obj;
    return (
      <div className="ui fraction-row page grid">
        <div className="name eight wide column">
          <img className="logo" src={fraction.logo_url}></img>
          {fraction.name}
        </div>
        <div className="two wide column">
          <div className="ui member statistic">
            <div className="value">{fraction.member_count}</div>
            <div className="label">narių</div>
          </div>
        </div>
        <div className="two wide column">
          <div className="ui discussion statistic">
            <div className="value">{fraction.avg_statement_count}</div>
            <div className="label">pasisaktmai</div>
          </div>
        </div>
        <div className="four wide column">
          <div className="ui projects statistic">
            <div className="value">{fraction.avg_passed_law_project_ratio}%</div>
            <div className="label">sėkmingų projektų</div>
          </div>
        </div>
        <div className="two wide column">
          <div className="ui voting statistic">
            <div className="value">{fraction.avg_vote_percentage}%</div>
            <div className="label">balsavimų vid.</div>
          </div>
        </div>
      </div>
    )
  }
});


React.render(
  <Switcher />,
  document.getElementById('fraction-filter-component')
);

