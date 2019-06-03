import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FlexLayoutModule } from '@angular/flex-layout';
import { SharedModule } from './shared/shared.module';
import { BookListComponent } from './books/book-list/book-list.component';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BookAddComponent } from './books/book-list/book-add/book-add.component';
import { ScrollingModule } from '@angular/cdk/scrolling';
import { RequestCache } from './shared/request.cache';
import { CachingInterceptor } from './shared/http.interceptor';

@NgModule({
  declarations: [
    AppComponent, BookListComponent, BookAddComponent
  ],
  imports: [
    AppRoutingModule,
    BrowserAnimationsModule,
    BrowserModule,
    ScrollingModule,
    HttpClientModule,
    SharedModule,
    FlexLayoutModule,
    FormsModule,
    ReactiveFormsModule
  ],
  entryComponents: [BookAddComponent],
  exports: [FlexLayoutModule],
  providers: [
    RequestCache,
    { provide: HTTP_INTERCEPTORS, useClass: CachingInterceptor, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
