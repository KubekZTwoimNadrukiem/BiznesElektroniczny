<?php
if (!defined('_PS_VERSION_')) {
    exit;
}

class Yarn_Payment extends Module {
public function __construct()
    {
        $this->name = 'yarn_payment';
        $this->tab = 'front_office_features';
        $this->version = '1.0.0';
        $this->author = 'KubekZMoimNadrukiem';
        $this->need_instance = 0;
        $this->ps_versions_compliancy = [
            'min' => '1.7.0.0',
            'max' => '8.99.99',
        ];
        $this->bootstrap = true;

        parent::__construct();

        $this->displayName = $this->trans('Yarnstreet payment options', [], 'Modules.Yarnpayment.Admin');
        $this->description = $this->trans('List of payment options.', [], 'Modules.Yarnpayment.Admin');

        $this->confirmUninstall = $this->trans('Are you sure you want to uninstall?', [], 'Modules.Yarnpayment.Admin');

        if (!Configuration::get('YARN_PAYMENT_NAME')) {
            $this->warning = $this->trans('No name provided', [], 'Modules.Yarnpayment.Admin');
        }
    }

public function install()
{
    if (Shop::isFeatureActive()) {
        Shop::setContext(Shop::CONTEXT_ALL);
    }

   return (
        parent::install()
	&& $this->registerHook('footer')
        && Configuration::updateValue('YARN_PAYMENT__NAME', 'yarn_payment')
    );
}

public function uninstall()
{
    return (
        parent::uninstall() 
        && Configuration::deleteByName('YARN_PAYMENT_NAME')
    );
}

public function hookDisplayFooter($params)
{
  $this->context->smarty->assign(
      array(
          'yarn_payment_name' => Configuration::get('YARN_PAYMENT_NAME'),
          'yarn_payment_link' => $this->context->link->getModuleLink('yarn_payment', 'display')
      )
  );
  return $this->display(__FILE__, 'yarn_payment.tpl');
}

public function hookDisplayHeader()
{
  $this->context->controller->addCSS($this->_path.'css/yarn_payment.css', 'all');
}


}
