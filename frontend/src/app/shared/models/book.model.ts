import { Author } from './author.model';
import { Series } from './series.model';
import { Genre } from './genre.model';

export class Book {
    id?: number;
    title: string;
    description?: string;
    author: Author;
    series?: Series[];
    genres?: Genre[];
}
