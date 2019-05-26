import { Author } from './author.model';
import { Series } from './series.model';
import { Genre } from './genre.model';

export interface Book {
    id?: number;
    title: string;
    description?: string;
    author: Author;
    series?: Series[];
    genres?: Genre[];
}
