import { Book } from './book.model';
import { Author } from './author.model';

export interface Series {
    id?: number;
    title: string;
    description?: string;
    books?: Book[];
    authors?: Author[];
}

export interface SeriesDTO {
    id?: number;
    title: string;
    description?: string;
    books_ids?: number[];
    authors_ids?: number[];
}
