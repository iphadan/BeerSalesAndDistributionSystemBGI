from django.urls import path
from .import views
urlpatterns = [
    path('', views.Admin_dashboard, name="admin-dashbord"),

    path('staff_dashboard', views.staff_dashboard, name="dashbord-staff"),
    path('store_dashboard', views.store_dashboard, name="dashbord-store"),
    path('region_dashboard', views.region_dashboard, name="dashbord-region"),
    path('product_dashboard', views.product_dashboard, name="dashbord-product"),


    path('show_profile/', views.show_profile, name='show_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('change_profile_pic/', views.change_profile_pic,
         name='change_profile_pic'),
    path('delete_profile_pic/', views.delete_profile_pic,
         name='delete_profile_pic'),

    # Agent Management Part
    path('add-agent/', views.add_agent, name='add-agent'),
    path('agent-view/', views.agent_view, name='agent-view'),
    path('agent-detail/<int:pk>', views.agent_detail, name='agent-detail'),
    path('update_contrat/<int:pk>',
         views.agent_update_contrat, name='update_contrat'),
    path('remove-agent/<int:pk>', views.remove_agent, name='remove-agent'),
    path('remove-agent_page/<int:pk>',
         views.remove_agent_page, name='remove_agent_page'),
    path('re-active_account/<int:pk>',
         views.re_active_account, name='re-active_account'),
    path('agent-report/', views.agent_report, name='agent-report'),
    path('view-agent-orders/', views.view_agent_orders, name='view-agent-orders'),
    path('approve-agent-orders/', views.approve_agent_orders,
         name='approve-agent-orders'),


    # end Agent Management Part

    # ////////////////////////

    # Manage Stafe

    path('view-staff/', views.view_staff, name='view-staff'),
    path('add-staff/', views.add_staff, name='add-staff'),
    path('staff-detail/<int:pk>/<str:staff>',
         views.staff_profile, name='staff-detail'),
    path('update-staff/<int:pk>/<str:staff>',
         views.update_staff, name='update-staff'),
    path('remove-staff/<int:pk>/<str:staff>',
         views.remove_staff, name='remove-staff'),
    path('staff_remove_page/<int:pk>/<str:staff>',
         views.staff_remove_page, name='staff_remove_page'),




    # end manage staff
    path('approve-agent-orders/', views.approve_agent_orders,
         name='approve-agent-orders'),
    path('store/', views.store, name='store'),
    path('contact-store-manager/', views.contact_store_manager,
         name='contact-store-manager'),
    path('finance-report/', views.finance_report, name='finance-report'),
    path('add_advertisments/', views.advertisments_view, name='add-advertisments'),
    path('post_advertisment/', views.post_advertisment, name='post_advertisment'),
    path('advertisements/', views.advertisements, name='advertisements'),


    # end manage-staff

    # deleted account

    path('deleted_account/', views. deleted_account, name='deleted_account'),
    path('permalent_delete/<int:pk>/',
         views. permalent_delete, name='permalent_delete'),

    # end deleted account



    # Manage store part

    path('view_store/', views.view_store, name='view-store'),
    path('add_store_company/', views.add_store_company, name='add-store-company'),
    path('store_detile/<int:pk>', views.sore_ditel_view, name="store_detile"),
    # end Manage store part

    # Manage region part

    path('view_region/', views.view_region, name='view-region'),
    path('add_region/', views.add_region, name='add-region'),
    path('detail_region/<int:pk>', views.RegionDetail, name='detail-region'),
    

    # endregion part

    # Manage Product

    path('view_product/', views.view_product, name='view-product'),
    path('add_product/', views.add_product, name='add-product'),
    path('update_product/<int:pk>', views.update_product, name='update-product'),
    path('delete_product_page/<int:pk>',views.delete_product_page, name='delete-product-page'),
    path('delete_product/', views.delete_product, name='delete_product'),
    path('product_update_pic_link/<int:pk>', views.product_update_pic_link, name='product_update_pic_link'),
    

    # End Product

    path('add_advertisments/', views.advertisments_view, name='add-advertisments'),
    path('add_ditel/<int:pk>', views.add_ditel, name='add_ditel'),
    path('delete_adds_post/<int:pk>', views.delete_adds_post, name='delete_adds_post'),
  
    # END Addivertisment


    # Report
    path('view_report/', views.view_report, name='view-report'),
    path('Store_Refill_Report/', views.storeRefillReport, name='Store_Refill_Report'),

    # END Report

    # store manager

    path('Store_Manager/', views.store_manager_view, name='store-manager-home'),
    path('Store_Manager/add_produc_to_store',
         views.add_produc_to_store_view, name='add-to-store'),
    path('Store_Manager/view_aproved_order',
         views.aprove_order_view, name='view-aprove-order'),
    path('Store_Manager/check_slip/<int:pk>',
         views.stor_check_slip_view, name='stor_check_slip_view'),
    path('Store_Manager/allow_load/<int:pk>',
         views.allow_load_view, name='allow_load'),
    path('Store_Manager/loaded_order', views.loaded_order, name='loaded-order'),



    # End Store manager


    # finance admin
    path('Finance_Admin/', views.finance_admin_view, name='finance_admin_home'),
    path('show_profile_finance/', views.show_profile_finance, name='show_profile_finance'),
    path('Finance_Admin/check_slip/<int:pk>',
         views.check_slip_view, name='check_slip_view'),
    path('Finance_Admin/approve/<int:pk>',
         views.approve_view, name='approve-order'),
    path('Finance_Admin/check_store',
         views.check_store_view, name='finance-check-store'),
    path('Finance_Admin/aprove_order_history',
         views.aprove_order_history_view, name='aprove-order-history'),

    # end finace admin
]
