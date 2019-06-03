import { DefaultQuery } from './models/query.model';

export const DEBOUNCE_TIME = 600;
export const PAGE_SIZES = [10, 20, 30, 40, 50];

export const DEFAULT_PARAMETERS: DefaultQuery = {
    direction: 'ASC',
    page: '1',
    per_page: '10',
    query_all: '',
    sort_column: 'id'
};
