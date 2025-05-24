import { Table, Terminal, PlugZap, Key, Settings, MessageCircle, Database } from 'lucide-react'
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarHeader,
  SidebarFooter
} from '@/components/ui/sidebar'
import logo from '@/assets/logo/logo.svg'
const sidebarItems = [
  { title: 'Chat', icon: MessageCircle, url: '/' },
  { title: 'Documents', icon: Terminal, url: '/documents' },
  { title: 'Evaluation', icon: Table, url: '/evaluation' },
  { title: 'Dataset', icon: Database, url: '/dataset' }
]
const bottomItems = [{ title: 'Settings', icon: Settings, url: '/settings' }]
const AppSidebar = () => {
  const sidebarSize = 'sm'
  return (
    <Sidebar>
      <SidebarHeader className='flex flex-row gap-2 items-center'>
        <img src={logo} alt='logo' className='w-7' />
        <p className='text-3xl font-medium'>BDA</p>
      </SidebarHeader>
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
      <SidebarFooter>
        <SidebarGroupLabel>Others</SidebarGroupLabel>
        <SidebarMenu>
          {bottomItems.map((item) => (
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
      </SidebarFooter>
    </Sidebar>
  )
}

export default AppSidebar
