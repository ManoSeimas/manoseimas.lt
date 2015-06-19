var Filter = React.createClass({
  getInitialState: function() {
    return {
      filter: 'name'
    };
  },

  render: function() {
    return (
      <div>
        <div className="filter">
          <ul>
            <li>Pavadinimas</li>
            <li>Aktyvumas</li>
            <li>Balsavimai</li>
            <li>Projektai</li>
          </ul>
        </div>
        <FractionList filter={this.state.filter} />
      </div>
    );
  }
});

var FractionList = React.createClass({
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

  render: function() {
    return (
      <div>
      {this.state.fractions.map(function (fraction) {
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

