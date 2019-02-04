import wx

if __name__ == '__main__':
    print 'Please don\'t run me'

def FnMenu(MenuItems, intID, boolDebug=False):
    menuFileMenu = wx.Menu()
    for item in MenuItems:
        if boolDebug: menuFileMenu.Append(intID, '%s %s' %(item, str(intID)))
        else: menuFileMenu.Append(intID, item)
        menuFileMenu.AppendSeparator()
        intID += 1

    return menuFileMenu, intID

def FnMenuBar(MenuBarItems, MenuItems):
    mbarMenuBar = wx.MenuBar()
    intcount = 0
    intID = 100        #100 --> 199 for menu items
    for item in MenuBarItems:
        if MenuItems[intcount]: menu, intID = FnMenu(MenuItems[intcount], intID, True)
        else: menu = wx.Menu()
        mbarMenuBar.Append(menu, item)
        intcount += 1

    return mbarMenuBar