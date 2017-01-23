import { Component } from '@angular/core';

import {SettingsPage} from "../settings/settings";
import {MyListingsPage} from "../my-listings/my-listings";
import {MainPage} from "../main/main";

@Component({
  templateUrl: '../tabs/tabs.html'
})
export class TabsPage {
  // this tells the tabs component which Pages
  // should be each tab's root Page
  tab1Root: any = MainPage;
  tab2Root: any = MyListingsPage;
  tab3Root: any = SettingsPage;

  constructor() {

  }
}
