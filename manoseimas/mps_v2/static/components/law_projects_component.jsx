var LawProjects = React.createClass({
  getInitialState: function() {
    return {
      projects: [],
      total_pages: 1,
      current_page: 1,
      items_per_page: 10
    }
  },

  componentDidMount: function() {
    $.get(this.props.data_url, function(result) {
      total_pages = Math.round((result.items.length / this.state.items_per_page)+0.5);

      if (this.isMounted()) {
        this.setState({
          projects: result.items,
          total_pages: total_pages
        })
      }
    }.bind(this))
  },

  onChangePage: function(page) {
    this.setState({current_page: page});
  },

  render: function() {
    var columns = {
      number: {title: 'Projekto numeris', func: null},
      title: {title: 'Pavadinimas', func: null },
      date: {title: 'Teikimo data', func: null },
      proposer_count: {title: 'Viso teikėjų', func: null },
      date_passed: {
        title: 'Priėmimas',
        func: function (value) {
          return (value) ? 'Priimtas '+value : 'Nepriimtas'
        }
      },
    }

    var slice_from = (this.state.current_page-1)*this.state.items_per_page,
        slice_to = this.state.current_page*this.state.items_per_page;

    return (
      <div className="law-projects">
        <div className="ui page grid">
          <div className="eight wide column">
            <h2 className="title">Įstatymų projektai</h2>
          </div>
          <div className="eight wide right aligned column">
            <Paginator max={this.state.total_pages} onChange={this.onChangePage} />
          </div>

          <div className="ui zero margin grid">
            <SemanticTable columns={columns}
                           items={this.state.projects.slice(slice_from, slice_to)} />
          </div>
        </div>
      </div>
    )
  }
});

var SemanticTable = React.createClass({
  render: function() {
    var columns = this.props.columns;
    return (
      <table className="ui zero paddings table">
        <thead>
          <tr>
            {Object.keys(columns).map(function (key) {
              return <th>{columns[key].title}</th>
            })}
          </tr>
        </thead>
        <tbody>
            {this.props.items.map(function (item) {
              return (
                <tr>
                  {Object.keys(columns).map(function (key) {
                    return (
                      <td>
                      {(columns[key].func) ? columns[key].func(item[key]) : item[key]}
                      </td>
                    )
                  })}
                </tr>
              )
            })}
        </tbody>
      </table>
    )
  }
});


var data_url = '/json/law_projects/' + $('#law-projects-component').attr("data-slug");

React.render(
  <LawProjects data_url={data_url} />,
  document.getElementById('law-projects-component')
);
