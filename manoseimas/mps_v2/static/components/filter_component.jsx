var Filter = React.createClass({
  getInitialState: function() {
    return {
      fractions: []
    };
  },

  componentDidMount: function() {
    $.get('/mp/fractions_json', function(result) {
      if (this.isMounted()) {
        this.setState({
          fractions: result.fractions
        });
      }
    }.bind(this))
  },

  sortElements: function (param) {
    var self = this;
    return function () {
      self.setState({
        fractions: self.state.fractions.sort(function (a, b) {
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
    return (
      <div>
        <div className="sort-keys">
          {sortkeys.forEach(function(sortkey) {
            return (
              <SortKeySelector params={sortkey}/>
            )
          })}
        </div>
        <FractionList fractions={this.state.fractions} />
      </div>
    );
  }
});

var SortKeySelector = React.createClass({
  render: function() {
    return (
      <div onClick={this.props.params.handler} className={this.props.params.active}>
        <i className={this.props.params.icon}></i>{this.props.params.title}
      </div>
    )
  }
});

var FractionList = React.createClass({
  render: function() {
    return (
      <div className="ui page grid">
      {this.props.fractions.map(function (fraction) {
        return (
          <Fraction obj={fraction} />
        )
      })}
      </div>
    );
  }
});

var Fraction = React.createClass({
  render: function() {
    var fraction = this.props.obj;
    return (
      <div className="fraction">
        <div className="name four wide column">
          <img className="logo" src={fraction.logo_url}></img>
          {fraction.name}
        </div>
        <div className="two wide column">
          <div className="ui members statistics">
            <div className="value">{fraction.member_count}</div>
            <div className="label">narių</div>
          </div>
        </div>
      </div>
    )
  }
});


React.render(
  <Filter />,
  document.getElementById('fraction-filter-component')
);

