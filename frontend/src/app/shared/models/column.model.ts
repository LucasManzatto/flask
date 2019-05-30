import { Book } from './book.model';

export class ColumnModel {
    columnDef: string;
    header: string;
    cell: (row: any) => string;
}
