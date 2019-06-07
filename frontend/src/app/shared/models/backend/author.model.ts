import { Book } from './book.model';
import { Series } from './series.model';

export interface Author {
    id?: number;
    name: string;
    books?: Book[];
    series?: Series[];
}

export interface AuthorDTO {
    id?: number;
    name: string;
    books_ids?: number[];
    series_ids?: number[];
}
