#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/netfilter.h>
#include <linux/netfilter_ipv4.h>
#include <linux/ip.h>
#include <linux/tcp.h>
#include <linux/udp.h>
#include <linux/if_ether.h>
#include <linux/inet.h>
#include <linux/icmp.h>
#include <linux/tcp.h>

// Implement two more hooks to achieve the following: (1) preventing other computers to ping the
// VM, and (2) preventing other computers to telnet into the VM. Please implement two different hook
// functions, but register them to the same netfilter hook. You should decide what hook to use.

static struct nf_hook_ops hook1, hook2, hook3, hook4, hook5, hook6, hook7, hook8;

// preventing other computers to ping the VM
unsigned int blockPing(void *priv, struct sk_buff *skb,
                       const struct nf_hook_state *state)
{
    struct iphdr *iph;
    struct icmphdr *icmph;

    if (!skb)
        return NF_ACCEPT;

    iph = ip_hdr(skb);
    icmph = icmp_hdr(skb);

    if (icmph->type == ICMP_ECHO)
    {
        printk(KERN_WARNING "*** Dropping %pI4 (ICMP_ECHO)\n", &(iph->daddr));
        return NF_DROP;
    }
    return NF_ACCEPT;
}

// preventing other computers to telnet into the VM
// Telnet’s default port is TCP port 23.
unsigned int blockTelnet(void *priv, struct sk_buff *skb,
                         const struct nf_hook_state *state)
{
    struct iphdr *iph;
    struct tcphdr *tcph;

    u16 port = 23;

    if (!skb)
        return NF_ACCEPT;

    iph = ip_hdr(skb);

    if (iph->protocol == IPPROTO_TCP)
    {
        tcph = tcp_hdr(skb);
        if (ntohs(tcph->dest) == port)
        {
            printk(KERN_WARNING "*** Dropping %pI4 (TCP), port %d\n", &(iph->daddr), port);
            return NF_DROP;
        }
    }
    return NF_ACCEPT;
}

unsigned int blockUDP(void *priv, struct sk_buff *skb,
                      const struct nf_hook_state *state)
{
    struct iphdr *iph;
    struct udphdr *udph;

    u16 port = 53;
    char ip[16] = "8.8.8.8";
    u32 ip_addr;

    if (!skb)
        return NF_ACCEPT;

    iph = ip_hdr(skb);
    // Convert the IPv4 address from dotted decimal to 32-bit binary
    in4_pton(ip, -1, (u8 *)&ip_addr, '\0', NULL);

    if (iph->protocol == IPPROTO_UDP)
    {
        udph = udp_hdr(skb);
        if (iph->daddr == ip_addr && ntohs(udph->dest) == port)
        {
            printk(KERN_WARNING "*** Dropping %pI4 (UDP), port %d\n", &(iph->daddr), port);
            return NF_DROP;
        }
    }
    return NF_ACCEPT;
}

unsigned int printInfo(void *priv, struct sk_buff *skb,
                       const struct nf_hook_state *state)
{
    struct iphdr *iph;
    char *hook;
    char *protocol;

    switch (state->hook)
    {
    case NF_INET_LOCAL_IN:
        hook = "LOCAL_IN";
        break;
    case NF_INET_LOCAL_OUT:
        hook = "LOCAL_OUT";
        break;
    case NF_INET_PRE_ROUTING:
        hook = "PRE_ROUTING";
        break;
    case NF_INET_POST_ROUTING:
        hook = "POST_ROUTING";
        break;
    case NF_INET_FORWARD:
        hook = "FORWARD";
        break;
    default:
        hook = "IMPOSSIBLE";
        break;
    }
    printk(KERN_INFO "*** %s\n", hook); // Print out the hook info

    iph = ip_hdr(skb);
    switch (iph->protocol)
    {
    case IPPROTO_UDP:
        protocol = "UDP";
        break;
    case IPPROTO_TCP:
        protocol = "TCP";
        break;
    case IPPROTO_ICMP:
        protocol = "ICMP";
        break;
    default:
        protocol = "OTHER";
        break;
    }
    // Print out the IP addresses and protocol
    printk(KERN_INFO "    %pI4  --> %pI4 (%s)\n",
           &(iph->saddr), &(iph->daddr), protocol);

    return NF_ACCEPT;
}

int registerFilter(void)
{
    printk(KERN_INFO "Registering filters.\n");

    hook1.hook = printInfo;
    hook1.hooknum = NF_INET_LOCAL_OUT;
    hook1.pf = PF_INET;
    hook1.priority = NF_IP_PRI_FIRST;
    nf_register_net_hook(&init_net, &hook1);

    hook2.hook = blockUDP;
    hook2.hooknum = NF_INET_POST_ROUTING;
    hook2.pf = PF_INET;
    hook2.priority = NF_IP_PRI_FIRST;
    nf_register_net_hook(&init_net, &hook2);

    // Hook the printInfo function to all of the netfilter hooks.
    // NF_INET_PRE_ROUTING
    // NF_INET_LOCAL_IN
    // NF_INET_FORWARD
    // NF_INET_LOCAL_OUT yes
    // NF_INET_POST_ROUTING
    hook3.hook = printInfo;
    hook3.hooknum = NF_INET_PRE_ROUTING;
    hook3.pf = PF_INET;
    hook3.priority = NF_IP_PRI_FIRST;
    nf_register_net_hook(&init_net, &hook3);

    hook4.hook = printInfo;
    hook4.hooknum = NF_INET_LOCAL_IN;
    hook4.pf = PF_INET;
    hook4.priority = NF_IP_PRI_FIRST;
    nf_register_net_hook(&init_net, &hook4);

    hook5.hook = printInfo;
    hook5.hooknum = NF_INET_FORWARD;
    hook5.pf = PF_INET;
    hook5.priority = NF_IP_PRI_FIRST;
    nf_register_net_hook(&init_net, &hook5);

    hook6.hook = printInfo;
    hook6.hooknum = NF_INET_POST_ROUTING;
    hook6.pf = PF_INET;
    hook6.priority = NF_IP_PRI_FIRST;
    nf_register_net_hook(&init_net, &hook6);

    // (1) preventing other computers to ping the VM
    hook7.hook = blockPing;
    hook7.hooknum = NF_INET_LOCAL_IN;
    hook7.pf = PF_INET;
    hook7.priority = NF_IP_PRI_FIRST;
    nf_register_net_hook(&init_net, &hook7);

    // (2) preventing other computers to telnet into the VM.
    hook8.hook = blockTelnet;
    hook8.hooknum = NF_INET_LOCAL_IN;
    hook8.pf = PF_INET;
    hook8.priority = NF_IP_PRI_FIRST;
    nf_register_net_hook(&init_net, &hook8);

    return 0;
}

void removeFilter(void)
{
    printk(KERN_INFO "The filters are being removed.\n");
    nf_unregister_net_hook(&init_net, &hook1);
    nf_unregister_net_hook(&init_net, &hook2);
    nf_unregister_net_hook(&init_net, &hook3);
    nf_unregister_net_hook(&init_net, &hook4);
    nf_unregister_net_hook(&init_net, &hook5);
    nf_unregister_net_hook(&init_net, &hook6);
    nf_unregister_net_hook(&init_net, &hook7);
    nf_unregister_net_hook(&init_net, &hook8);
}

module_init(registerFilter);
module_exit(removeFilter);

MODULE_LICENSE("GPL");
