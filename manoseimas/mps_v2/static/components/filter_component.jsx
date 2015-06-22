var Filter = React.createClass({
  getInitialState: function() {
    return {
      items: [],
      total_pages: 1,
      current_page: 1,
      items_per_page: 20,
      active_filter: null,
      loaded: false
    };
  },

  componentDidMount: function() {
    if (this.isMounted()) this.loadData(this.props.endpoint);
  },

  loadData: function(endpoint) {
    $.get(endpoint, function(result) {
      total_pages = Math.round((result.items.length / this.state.items_per_page)+0.5);

      this.setState({
        items: result.items,
        loaded: true,
        total_pages: total_pages,
      });
    }.bind(this))
  },

  componentWillReceiveProps: function (nextProps) {
    this.setState({loaded: false, current_page: 1});
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
        }),
        active_filter: param
      })
    }
  },

  onChangePage: function(page) {
    this.setState({current_page: page});
    $.scrollTo('#fraction-filter-component', 100, {offset: -40})
  },

  render: function() {
    var sortkeys = this.props.keys,
        self = this,
        slice_from = (this.state.current_page-1)*this.state.items_per_page,
        slice_to = this.state.current_page*this.state.items_per_page;

    return (
      <div>
        <div className="ui zero margin page grid sort-keys">
          {sortkeys.map(function(sortkey, index) {
            // Creating proper class for sort keys using Semantic UI framework.
            column_count = (index === 0) ? 'eight' : 'two';
            active = (self.state.active_filter === sortkey.key) ? 'active ' : '';
            class_name = active + column_count + ' wide center aligned column'

            return (
              <SortKeySelector params={sortkey}
                               class_name={class_name}
                               handler={self.sortElements(sortkey.key)} />
            )
          })}
        </div>
        <Loader loaded={this.state.loaded}>
          <ElementList items={this.state.items.slice(slice_from, slice_to)} rowComponent={this.props.rowComponent} />
        </Loader>
        <div className={((this.state.total_pages < 2) ? 'hidden ' : '') + 'ui zero margin center aligned grid'}>
          <Paginator max={this.state.total_pages} onChange={this.onChangePage}/>
        </div>
      </div>
    );
  }
});

var SortKeySelector = React.createClass({
  render: function() {
    return (
      <div className={this.props.class_name}>
        <a onClick={this.props.handler}>
          {this.props.params.title}
        </a>
      </div>
    )
  }
});

var ElementList = React.createClass({
  render: function() {
    var self = this;
    return (
      <div className="filtered-elements">
      {self.props.items.map(function (item) {
        return (
          <self.props.rowComponent obj={item} />
        )
      })}
      </div>
    );
  }
});
