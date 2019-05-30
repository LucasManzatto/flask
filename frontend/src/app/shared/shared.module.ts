import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatTabsModule } from '@angular/material/tabs';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatInputModule } from '@angular/material/input';
import { MatSortModule } from '@angular/material/sort';
import { MatButtonModule } from '@angular/material/button';
@NgModule({
    declarations: [],
    imports: [CommonModule],
    exports: [MatIconModule, MatToolbarModule, MatFormFieldModule, MatInputModule,
        MatTabsModule, MatTableModule, MatPaginatorModule, MatSortModule, MatButtonModule],
    providers: [],
})
export class SharedModule { }
