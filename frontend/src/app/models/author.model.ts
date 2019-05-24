import { Book } from './book.model';
import { Series } from './series.model';

export interface Author {
    id?: number;
    name: string;
    books?: Book[];
    series?: Series[];
}
