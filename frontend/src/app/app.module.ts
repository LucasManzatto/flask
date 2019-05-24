import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {FlexLayoutModule} from '@angular/flex-layout';
import {SharedModule} from './shared/shared.module';
import { BookListComponent } from './book-list/book-list.component';

@NgModule({
  declarations: [
    AppComponent, BookListComponent
  ],
  imports: [
    AppRoutingModule, BrowserAnimationsModule, BrowserModule, SharedModule, FlexLayoutModule
  ],
  exports: [FlexLayoutModule],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
