import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FlexLayoutModule } from '@angular/flex-layout';
import { SharedModule } from './shared/shared.module';
import { BookListComponent } from './books/book-list/book-list.component';
import { MatTableModule } from '@angular/material/table';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { BookAddComponent } from './books/book-list/book-add/book-add.component';

@NgModule({
  declarations: [
    AppComponent, BookListComponent, BookAddComponent
  ],
  imports: [
    AppRoutingModule, BrowserAnimationsModule, BrowserModule, HttpClientModule, SharedModule, FlexLayoutModule, FormsModule
  ],
  entryComponents: [BookAddComponent],
  exports: [FlexLayoutModule],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
