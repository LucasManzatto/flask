import { MatButtonModule, MatToolbarModule, MatTableModule } from '@angular/material';
import { NgModule } from '@angular/core';

@NgModule({
    imports: [MatButtonModule, MatToolbarModule, MatTableModule],
    exports: [MatButtonModule, MatToolbarModule, MatTableModule],
})
export class MaterialModule { }
