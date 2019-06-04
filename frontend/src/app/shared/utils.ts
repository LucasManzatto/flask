import { Query } from './models/query.model';
import { defer } from 'rxjs';
export const createQuery = (object: any[]): Query => {
    const query: Query = {
        items: object,
        page: 1,
        per_page: 10,
        total: object.length
    };
    return query;
};

export function asyncData<T>(data: T) {
    return defer(() => Promise.resolve(data));
}
