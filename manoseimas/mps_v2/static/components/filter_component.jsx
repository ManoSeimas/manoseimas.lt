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
    return (
      <div>
        <div className="filter">
          <ul>
            <li><a onClick={this.sortElements('name')}>Pavadinimas</a></li>
            <li><a onClick={this.sortElements('avg_statement_count')}>Pasisakymai</a></li>
            <li><a onClick={this.sortElements('avg_vote_percentage')}>Balsavimai</a></li>
            <li><a onClick={this.sortElements('avg_passed_law_project_ratio')}>Projektai</a></li>
          </ul>
        </div>
        <FractionList fractions={this.state.fractions} />
      </div>
    );
  }
});

var FractionList = React.createClass({
  render: function() {
    return (
      <div>
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
    return (
      <div className="fraction">
        Hello, {this.props.obj.name}!
      </div>
    );
  }
});


React.render(
  <Filter />,
  document.getElementById('fraction-filter-component')
);

