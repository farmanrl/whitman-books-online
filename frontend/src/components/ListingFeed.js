import React, { Component } from 'react';
import { withRouter } from 'react-router-dom';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import Feed from './Feed';
import ListingItem from './ListingItem';
import { getListingList } from '../redux/listings/actions';
import { makeGetListingListByIds } from '../redux/listings/selectors';
import sampleData from '../redux/sampleData';

class ListingFeed extends Component {
  componentDidMount() {
    const { getListingList, listingIds } = this.props;
    getListingList({ listingIds });
  }

  render() {
    const { listingList, bookTitle, bookAuthor } = this.props;
    const loading = !Object.keys(listingList).length;

    return (
      <div>
        <Feed loading={loading} feedList={listingList} FeedItem={ListingItem} bookTitle={bookTitle} bookAuthor={bookAuthor}/>
      </div>
    );
  }
}

const makeMapStateToProps = () => {
  const getListingListByIds = makeGetListingListByIds();
  const mapStateToProps = (state, props) => {
    return {
      listingList: getListingListByIds(state, props),
    };
  };
  return mapStateToProps;
};

const mapDispatchToProps = dispatch =>
  bindActionCreators({ getListingList }, dispatch);

export default withRouter(connect(makeMapStateToProps, mapDispatchToProps)(ListingFeed));
