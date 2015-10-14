var lt_pluralize = function(n, singular, plural1, plural2) {
    if (n % 10 == 1 && n % 100 != 11) {
        return singular;
    } else if (n % 10 >= 2 && (n % 100 < 10 || n % 100 >= 20)) {
        return plural1;
    } else {
        return plural2;
    }
}

var num_to_word = function(num) {
    dict = {
        1: 'one',
        2: 'two',
        3: 'three',
        4: 'four',
        5: 'five',
        6: 'six',
        7: 'seven',
        8: 'eight',
        9: 'nine',
        10: 'ten',
        11: 'eleven',
        12: 'twelve',
        13: 'thirteen',
        14: 'fourteen',
        15: 'fifteen',
        16: 'sixteen'
    }
    return dict[num]
};

var PaliamentarianRow = React.createClass({
  render: function() {
    var parliamentarian = this.props.obj;
    var width_class = num_to_word(this.props.leading_column_width);
    var leading_column_class = 'name '+ width_class + ' wide column';
    return (
      <div className="ui parliamentarian-row zero margin page grid">
        <div className={leading_column_class}>
          <img className="photo" src={parliamentarian.photo}></img>
          <div className="info">
            <h2><a href={parliamentarian.url}>{parliamentarian.full_name}</a></h2>
            <p><a href={parliamentarian.fraction_url}>{parliamentarian.fraction_name}</a></p>
          </div>
        </div>
        <div className="two wide column">
          <div className="ui voting statistic">
            <div className="value">{parliamentarian.vote_percentage}%</div>
            <div className="label">balsavimų</div>
          </div>
        </div>
        <div className="two wide column">
          <div className="ui discussion statistic">
            <div className="value">{parliamentarian.statement_count}</div>
            <div className="label">
              {lt_pluralize(parliamentarian.statement_count, 'pasisakymas', 'pasisakymai', 'pasisakymų')}
            </div>
          </div>
        </div>
        <div className="two wide column">
          <div className="ui projects statistic">
            <div className="value">{parliamentarian.passed_law_project_ratio}%</div>
            <div className="label">priimta projektų</div>
          </div>
        </div>
      </div>
    )
  }
});

var FractionRow = React.createClass({
  render: function() {
    var fraction = this.props.obj;
    var width_class = num_to_word(this.props.leading_column_width);
    var leading_column_class = 'name '+ width_class + ' wide column';
    return (
      <div className="ui fraction-row zero margin page grid">
        <div className={leading_column_class}>
          <img className="logo" src={fraction.logo_url}></img>
          <div className="info">
            <h2><a href={fraction.url}>{fraction.name}</a></h2>
          </div>
        </div>
        <div className="two wide column">
          <div className="ui member statistic">
            <div className="value">{fraction.member_count}</div>
            <div className="label">
              {lt_pluralize(fraction.member_count, 'narys', 'nariai', 'narių')}
            </div>
          </div>
        </div>
        <div className="two wide column">
          <div className="ui voting statistic">
            <div className="value">{fraction.avg_vote_percentage}%</div>
            <div className="label">balsavimų</div>
          </div>
        </div>
        <div className="two wide column">
          <div className="ui discussion statistic">
            <div className="value">{fraction.avg_statement_count}</div>
            <div className="label">
              {lt_pluralize(fraction.avg_statement_count, 'pasisakymas', 'pasisakymai', 'pasisakymų')}
            </div>
          </div>
        </div>
        <div className="two wide column">
          <div className="ui projects statistic">
            <div className="value">{fraction.avg_passed_law_project_ratio}%</div>
            <div className="label">priimta projektų</div>
          </div>
        </div>
      </div>
    )
  }
});

var LobbyistRow = React.createClass({
  render: function() {
    var lobbyist = this.props.obj;
    var width_class = num_to_word(this.props.leading_column_width);
    var leading_column_class = 'name '+ width_class + ' wide column';
    return (
      <div className="ui fraction-row zero margin page grid">
        <div className={leading_column_class}>
          <div className="info">
            <h2><a href={lobbyist.url}>{lobbyist.name}</a></h2>
          </div>
        </div>
        <div className="two wide column">
          <div className="ui project statistic">
            <div className="value">{lobbyist.law_project_count}</div>
            <div className="label">
              {lt_pluralize(lobbyist.law_project_count, 'įstatymas', 'įstatymai', 'įstatymų')}
            </div>
          </div>
        </div>
        <div className="two wide column">
          <div className="ui client statistic">
            <div className="value">{lobbyist.client_count}</div>
            <div className="label">
              {lt_pluralize(lobbyist.client_count, 'užsakovas', 'užsakovai', 'užsakovų')}
            </div>
          </div>
        </div>
      </div>
    )
  }
});


var SuggesterRow = React.createClass({
  render: function() {
    var fraction = this.props.obj;
    var width_class = num_to_word(this.props.leading_column_width);
    var leading_column_class = 'name '+ width_class + ' wide column';
    return (
      <div className="ui fraction-row zero margin page grid">
       <div className={leading_column_class}>
          <div className="info">
            <h2><a href={fraction.url}>{fraction.name}</a></h2>
          </div>
        </div>
        <div className="two wide column">
          <div className="ui member statistic">
            <div className="value">{fraction.member_count}</div>
            <div className="label">
              {lt_pluralize(fraction.member_count, 'įstatymas', 'įstatymai', 'įstatymų')}
            </div>
          </div>
        </div>
        <div className="two wide column">
          <div className="ui voting statistic">
            <div className="value">{fraction.avg_vote_percentage}%</div>
            <div className="label">pastabų</div>
          </div>
        </div>
        <div className="two wide column">
          <div className="ui projects statistic">
            <div className="value">{fraction.avg_passed_law_project_ratio}%</div>
            <div className="label">priimta projektų</div>
          </div>
        </div>
      </div>
    )
  }
});
