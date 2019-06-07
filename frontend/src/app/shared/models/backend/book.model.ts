import { Author } from './author.model';
import { Series } from './series.model';
import { Genre } from './genre.model';

export class Book {
    id?: number;
    title: string;
    author: Author;
    description: string;
    series?: Series;
    genres?: Genre[];
}

export class BookDTO {
    id?: number;
    title: string;
    author_id: number;
    description: string;
    series_id?: number;
}
