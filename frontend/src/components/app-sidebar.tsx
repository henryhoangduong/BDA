import { Home, Terminal, PlugZap, Key, Settings, HelpCircle, HardDrive } from 'lucide-react'
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem
} from '@/components/ui/sidebar'
const sidebarItems = [
  { title: 'Home', icon: Home, url: '/' },
  { title: 'Documents', icon: Terminal, url: '/documents' },
  { title: 'Plugins', icon: PlugZap, url: '/plugins' },
  { title: 'API Keys', icon: Key, url: '/api-keys' },
  { title: 'Settings', icon: Settings, url: '/settings' }
]

const bottomItems = [
  { title: 'Help', icon: HelpCircle, url: '/help' },
  { title: 'Storage', icon: HardDrive, url: '/storage' }
]
const AppSidebar = () => {
  return (
    <Sidebar>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Application</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {sidebarItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <a href={item.url}>
                      <item.icon />
                      <span>{item.title}</span>
                    </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  )
}

export default AppSidebar
