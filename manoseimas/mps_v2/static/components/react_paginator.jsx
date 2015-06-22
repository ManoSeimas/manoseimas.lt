var Paginator = React.createClass({
  propTypes: {
      max: React.PropTypes.number.isRequired,
      maxVisible: React.PropTypes.number,
      onChange: React.PropTypes.func.isRequired
  },
  componentDidUpdate: function(prevProps, prevState) {
      if (prevState.currentPage !== this.state.currentPage) {
          this.props.onChange(this.state.currentPage);
      }
  },
  getDefaultProps: function() {
      return {
          maxVisible: 5
      };
  },
  getInitialState: function() {
      return {
          currentPage: 1,
          items: []
      };
  },
  goTo: function(page, e) {
      if (e) {
        e.preventDefault();
      }

      this.setState({currentPage: page});
  },
  onClickNext: function(e) {
      e.preventDefault();

      var page = this.state.currentPage;

      if (page < this.props.max) {
          this.goTo(page + 1);
      }
  },
  onClickPrev: function(e) {
      e.preventDefault();

      if (this.state.currentPage > 1) {
          this.goTo(this.state.currentPage - 1);
      }
  },
  render: function() {
      var className = this.props.className || '',
          p = this.props,
          s = this.state,
          skip = 0;

      if (p.max < p.maxVisible) p.maxVisible = p.max;
      if (s.currentPage > p.maxVisible - 1 && s.currentPage < p.max) {
          skip = s.currentPage - p.maxVisible + 1;
      } else if (s.currentPage === p.max) {
          skip = s.currentPage - p.maxVisible;
      }

      var iterator = Array.apply(null, Array(p.maxVisible)).map(function(v, i) {
          return skip + i + 1;
      });

      var showPrev = (s.currentPage === 1) ? 'disabled' : '';
      var showNext = (s.currentPage === p.max) ? 'disabled' : '';

      return (
          <div className={'ui pagination menu' + className}>
              <a href="#"
                  className={'item ' + showPrev}
                  onClick={this.onClickPrev}>
                  <i className="left arrow icon"></i> Atgal
              </a>
              {iterator.map(function(page) {
                  return (
                      <a href="#"
                          key={page}
                          onClick={this.goTo.bind(this, page)}
                          className={s.currentPage === page ? 'item active' : 'item'}>
                          {page}
                      </a>
                  );
              }, this)}
              <a href="#"
                  className={'item ' + showNext}
                  onClick={this.onClickNext}>
                  <i className="right arrow icon"></i> Pirmyn
              </a>
          </div>
      );
  }
});
